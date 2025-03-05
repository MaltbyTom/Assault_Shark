# They Comin

2D scrolling flight shooter inspired by the aesthetic of 80's arcade games
Written by Tom Maltby, attributions for components follow
www.maltby.org
currently 1380 lines, written in one forty hour weekend of coding

## Gameplay Gif

![they comin gif](https://github.com/user-attachments/assets/739a6257-07a0-4942-954c-34ba4292b26a)

## License

(MIT License)

Copyright (c) 2025 Tom Maltby

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Description

Barring 2 hours last summer, this is my first Python coding, and my first significant coding in any language
in the last 15 years.  There are a lot of things that should be made more elegant.  Graphics and fonts and sounds
are loaded as needed rather than being cached.  A lot of things should be further object oriented.  I haven't 
looked into Python's best practice file / directory structure, etc.  This is the result of an initial 40 hour 
coding blast over a weekend, starting as proof of concept and then repeatedly throwing a few hours at the most 
synchronous next topic for maximum effect in available time.  

Hopefully I will keep finding time to put some of those organizational improvements in, as well as to implement some
of my desired feature list that I haven't gotten to.  It's a fun game.  

Based off Jon Fincher's 120 line tutorial py_tut_with_images.py
py_tut_with_images on github: https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py
Jon's blog: https://realpython.com/pygame-a-primer/

Additional sounds from  http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
Arcade font from https://www.dafont.com/arcade-ya.font , by Yuji Adachi, listed as 100% free

Thanks to Jon for the neat demo of a viable set of tools, and to the creators of the great font, sounds, and music.

Graphics except jet, missile, and white cloud are by me, using Corel and Gimp.
 

## Installation instructions:

### Requirements:

pygame-ce 2.5.3 (SDL 2.30.12, Python 3.12.2)

### Step by step instructions:

Create a folder for installation, such as C:\theycomin

Place downloaded files in the folder.

From the folder, create a venv, such as:

```
python -m venv venv
```

Activate the venv:

```
.venv\scripts\activate.bat
```

Install requirements:

```
pip install -r requirements.txt
```

## Update log:
(Pre Github)

### 2/28/2025

* Missile movement climb/dive, variance
* Plane shoots
* Diverse collision tree
* Bio, Blaster, Shock Shield added
* collision tree improved
* Powerups added
* Powerup collision results
* Initial game status text bars


### 3/1/2025

* Sounds for each event type
* Start screen, press enter to play
* Added Pulsar, powerup
* Added Sun, Moon
* Added waves, darkening sky
* Added blimps
* Significant motion improvements, limits
* Added hp (1 missiles, 10 blimp, 20 armored blimp - red)
* Involved collision result updates
* Added homing missiles
* Blimps shoot homing missiles
* Blimps spawn more often in later waves
* Blimps shoot more often in later waves
* High score and save file
* Create sounds folder
* Create graphics folder

### 3/2/2025

* Discovered updating the rect attribute after resizing fixes the collision errors with growing bullets such as bio
* Added mountains/towers
* Added guns on mountains/towers
* Worked out impacts on towers for bullets/enemies/player
* Weighted spawn rate with wave
* Next life / next wave pauses more dramatic with red/green flash and countdown on screen
* Added player health and armor
* Integrated status bar with health and armor bars
* Added health and armor power ups
