import pygame  # type: ignore
pygame.init()
from random import randint, uniform
import os
import sys

#------import------#
star = pygame.image.load('star.png')
meteor = pygame.image.load('meteor.png')
laser = pygame.image.load('laser.png')
explosion_frames = [pygame.image.load(f'{i}.png') for i in range(21)]
laser_awaz = pygame.mixer.Sound('laser.wav')
explosion_a = pygame.mixer.Sound('explosion.wav')
damage_a = pygame.mixer.Sound('damage.ogg')
gaana = pygame.mixer.Sound('game_music.wav')
gaana.play(loops = -1)

#------general setup------#
score = 0
clock = pygame.time.Clock()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space shooter')
font = pygame.font.Font('font.ttf', 40)
text = font.render(f'Score: {score}', True, 'white')
running = False
run = True
is_over = False

#------Classes------#
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect(center = (width / 2, height-100))
        self.direction = pygame.Vector2()
        self.speed = 600

        # cooldown 
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  
        self.direction = self.direction.normalize() if self.direction else self.direction 
        if self.rect.centerx + self.speed*dt < width and self.rect.centerx + self.speed*dt>0 and self.rect.centery+self.speed*dt>0 and self.rect.centery+self.speed*dt<height:
            self.rect.center += self.direction * self.speed * dt
        else:
            if self.rect.centerx<width/2:
                self.rect.centerx = width-1
            elif self.rect.centerx>width/2:
                self.rect.centerx = 1
            elif self.rect.centery>height/2:
                self.rect.centery=1
            elif self.rect.centery<height/2:
                self.rect.centery = height-1

        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser, self.rect.midtop, (all_sprites, laser_sprites)) 
            laser_awaz.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.speed = 600

    def update(self, dt):
        self.rect.centery+=self.speed*dt
        if self.rect.top>height:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_rect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 800 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.original_surf = surf
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(600,700)
        self.rotation_speed = randint(40, 50)
        self.rotation = 0
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top>height:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center = self.rect.center)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frame, pos, groups):
        super().__init__(groups)
        self.frame = frame
        self.index = 0
        self.image = self.frame[self.index]
        self.rect = self.image.get_rect(center = pos)

    def update(self, dt):
        self.index+=20*dt
        if self.index<len(self.frame):
            self.image = self.frame[int(self.index)]
        else:
            self.kill()
        

#------Collisions------#
def collisions():
    global running 
    global is_over
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprites:
        player.kill()
        player.rect.center = (width+500, height+500)
        explosion_a.play()
        is_over = True
        Explosion(explosion_frames, player.rect.center, all_sprites)
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            explosion_a.play()
            Explosion(explosion_frames, laser.rect.midtop, all_sprites)

def display_score():
    global score
    time = pygame.time.get_ticks()
    if not is_over:
        score = time
    text = font.render(f'{score}', True, 'white')
    text_rect = text.get_rect(center = (width/2, height-50))
    window.blit(text, text_rect)

def restart_program():
    """Restart the current program."""
    python = sys.executable  # Path to the Python interpreter
    os.execv(python, [python] + sys.argv)  # Restart the script with the same arguments

#------sprites------#
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
player = Player(all_sprites)

# Star event
star_event = pygame.event.custom_type()
pygame.time.set_timer(star_event, 500)

# meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

#Game over text
overtext = font.render('GAME OVER!', True, 'white')
overtext2 = font.render('Press O to restart', True, 'white')
overtext_rect = overtext.get_rect(center = (width/2, -60))
overtext2_rect = overtext2.get_rect(center = (width/2, -10))

#_______GAME LOOP_______#

while run:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                running = True
                run = False
    
    window.fill('black')

    for i in range(2):
        window.blit(star, (randint(0, width), randint(0, height)))
    hometext = font.render("Messiah", True, 'white')
    hometext2 = font.render("Press o to begin", True, 'white')
    hometext_rect = hometext.get_rect(center = (width/2, height/2))
    hometext_rect2 = hometext.get_rect(center = (width/2-60, height-100))
    window.blit(hometext, hometext_rect)
    window.blit(hometext2, hometext_rect2)
    pygame.display.update()

while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, width), randint(-200, -100)
            Meteor(meteor, (x, y), (all_sprites, meteor_sprites))
        if event.type == star_event:
            for i in range(10):
                Star(star, (randint(0, width), randint(-1000, 0)), (all_sprites))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                running = False
                run = True
                restart_program()
                   
    # update
    all_sprites.update(dt)
    collisions()

    # draw the game
    window.fill('black')
    all_sprites.draw(window)
    display_score()
    # Gameover
    if is_over and overtext_rect.centery<=height/2:
        overtext_rect.centery+=1
        overtext2_rect.centery+=1
        window.blit(overtext, overtext_rect)
        window.blit(overtext2, overtext2_rect)
    if is_over and overtext_rect.centery>height/2:
        window.blit(overtext, overtext_rect)
        window.blit(overtext2, overtext2_rect)
    
    pygame.display.update()


pygame.quit()
