# Messiah<br>
<br>
Messiah is a game moreover similar to the epic space shooter game which we all must have played atleast once in our life..<br>
The main code is written in play.py<br>
Other files are supportive like they include images, sounds, and the files named 0 to 20 are the frames for explosion..<br>
You can press o to begin and after the game ends, again press o to restart.<br>
However while playing, you will may feel like the game is on hard mode so for that, you have the whole code just edit the speeds or count of meteoroids or you can even try reducing fps <br>however it is not recommended.<br>
Still there may be few bugs which i will update with the passage of time..<br>
Also your score is the time you survived in the game in miliseconds.<br>
There is a bit loophole also, you can teleport to the left part just by moving out through the right and vice-versa is also true.<br>
<br>
Enjoy playing..<br>
<br>
<br>
Game Description:<br>
There are classes for player, rocks, laser, stars, explsosion...I have used some youtube videos to learn pygame and moreover i have learned from its documentation..<br>
I have used sprite in all classes to make a collection of them for general setup.<br>
each object is associated with an invisible rect which to used to detect collision and to make smoother movements.<br>
Each class has its update function which i use sprite.update() in the game loop to run this all together..<br>
To check collisions , display score and to restart the game i have made seperate functions..<br>
i have made seperate Sprite groups for meteor and lasers so that i can detect their collsion easily like meteoroids and player and meteroids and laser..<br>
I have not specified any fps so that it remain compatible with all devices. In place of that it will make use of the general fps of the system and so that it works same on all devices i have made all movements dependent on dt time which you will see in the code.<br>
However i have titles before any new topic and ig the code is also not so messy so you can read and you will get my idea..<br>
<br>
How to play:<br>
If you are ready to run the code, the you are just some clicks away..<br>
Run it and now you have the choice to be a messiah. click 'o' and now all eyes are on you.<br>
RIGHT - To move right and same for all direction keys<br>
SPACE - to fire laser<br>
O - to return to home screen<br>
That's all and now you are ready to save the universe..<br>
<br>
Credits:<br>
Some youtube videos like the 20 videos playlist of codewithharry to make snake game.. and many more..<br>
Pygame documentary was also proved helpful..<br>
<br>
Thanks for your time..<br>
