# Assault Shark 

2D scrolling flight shooter inspired by the aesthetic of 80's arcade games.  

Jet powered sea creatures fight for dominance of the skies.

Written by Tom Maltby, attributions for components follow

www.maltby.org

## Gameplay Videos

Full demo video of 4/4/25 upgrade at https://www.maltby.org/images/AssaultShark.mp4

Now with three slots of multitiered MG upgrades, blowaway graphics, save / load functionality with 
savepoints in portals, screen backgrounds, pilot initials tracking, and the first BoxiPyg controls 
from my growing UI constructor library.

Assault Shark, as of 3/15/25 update:

![Assault Shark](https://github.com/user-attachments/assets/0baaeea0-21fb-48f9-bb9f-34dddfaa4023)


Original 40 hour game while first learning Python:

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

Now with blowaway graphics, save / load functionality with savepoints in portals, screen backgrounds,
and the first BoxiPyg controls from my growing UI constructor library.

Bosses have a special tentacle attack!  Egg laying rocket fish.  3 slots of upgrades
for the machine gun, each with multiple levels of upgrade.  New enemies can be added
with just a .json file and images.

Boss fights at the end of each wave, and reward showers of power ups after each
wave's boss is killed!  This is a huge update.  A highlight is that all enemy and 
bullet types are now stored in dictionaries, and their behavior is determined from 
polling those dictionaries.  Also lots more enemy types, animations, explosions, 
sparkly powerups that increase max health and armor, controller support (imported,
MIT license, by Jon Cooper, credits below), and lots more.  A full update log is also 
included below.

Also, I found my unifying theme:  evil jet powered marine creatures fighting to rule
the sky, supported by artillery.  Plot narrative is being hashed out: something on
the order of the last noble Assault Shark pilot from the mystic order of Sharknights,
saving the Republic from the Evil Empire's legions of biological horrors (completely
unlike assault sharks, obviously), and their kleptofascist groundling artillery support.

Barring 2 hours last summer, this is my first Python coding, and my first 
significant coding in any language in the last 15 years.  There are a lot of 
things that should be made more elegant.  A lot of things still should be further object 
oriented.  I haven't looked into Python's best practice file / directory structure,
etc.  This is the result of an initial 40 hour coding blast over a weekend.  It started 
as proof of concept and then grew through repeatedly throwing a few hours at the most 
synchronous next topic for maximum effect in available time.  This update significantly
organized the code, and then used that to almost triple the size of the code base.

Hopefully I will keep finding time to put some of those organizational improvements 
in, as well as to implement some of my desired feature list that I haven't gotten to.

It's a fun game.  My teenage child, who is the primary playtester, put up a 
high score just over 100K, and made it to wave 23.

Further credits:
* Original game based off Jon Fincher's 120 line tutorial py_tut_with_images.py 
* on github: https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py
* Additional sounds from  http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
* Arcade font from https://www.dafont.com/arcade-ya.font , by Yuji Adachi, listed as 100% free
* Joystick handling imported under MIT license:  Copyright (c) 2017 Jon Cooper
* pygame-xbox360controller - Documentation, related files, and licensing can be found at
* https://github.com/joncoop/pygame-xbox360controller>.


Thanks to Jon Fincher for the neat demo of a viable set of tools, and to the creators of the great 
font, sounds, and music.  Thanks to Jon Cooper for joystick code.

Graphics except white cloud are by me, using Corel and Gimp.
 

## Installation instructions:

### Requirements:

Python 3.12.2

pygame-ce 2.5.3 

pip

### Step by step instructions:

Create a folder for installation, such as C:\assaultshark

Place downloaded files in the folder.

From the folder, create a venv, such as:

```
python -m venv venv
```

Activate the venv:

```
venv\scripts\activate.bat
```

Install requirements:

```
pip install -r requirements.txt
```
Run the game
```
Python assaultshark.py
```

## Update log:

### 3/19/2025
* Template for new enemy .json files
* Added enemies
* Added egg laying mechanic
* Added first egg laying enemy (blue rocket fish)

### 3/18/2025
* Finished .json compatability reworking of dictionaries

### 3/17/2025
* Finished 3 slots of multi-level machine gun upgrades
* Improved MG panel display

### 3/16/2025
* Finished tentacle attack boss special weapon
* Improved advanced movement

### 3/14/2025
* Added bossfight mechanics
* Added bossfight healthbar with blinking border
* Added first advanced movement routine
* Added reward shower for end of bossfights
* Added boss and immunities flags to enemy dictionary entries
* Modified collision rebound effects
* Added iseveryonedead checker to catch wave end when odd timing
* Paused music on pause screen
* Large weapon effects degrade as they strike enemies

### 3/13/2025
* Animated sparkles for extra life powerup
* Added increase max health and armor mechanics
* Added powerups for increase max health/armor with animated sparkles
* Added red layer to pause/control text for visibility on  night levels
* Added controller support, imported under MIT license from Jon Cooper
* Graphics for first level boss

### 3/12/2025
* Firing behavior, ammo type, and movement all handled by dictionaries
* Replaced missiles from blimps with rocket powered fish and sneks
* Added animated graphics for fish and sneks
* Animated explosions for cannon and missile launchers
* Replaced jet with Assault Shark

### 3/11/2025
* Finished dictionary for enemy types
* Dictionary for bullet types
* Collisions handled by dictionary calls
* Animation & explosions handled by dictionaries

### 3/10/2025
* Added rocket launchers, created graphics
* Moved homing missile ammo type to rocket launchers
* Created skyburst ammo type and movement pattern for cannon
* Retooled shock shield - tracks with player, jumps gaps to nearby enemies
* Began dictionary for enemy types

### 3/7/2025
* Animated blinking light on nose cone of homing missile
* Stopped background sounds before player collision or wavechange sounds

### 3/6/2025 - housekeeping & play balance

* All graphics preloaded into a dictionary
* All fonts preloaded, all text that isn't a variable merge pre-rendered
* From user reccomendations, early waves now start slower 
    * using a % of wave completed factor + wave number squared
* Guns spawn less often in early waves
* Mountains / Guns now blocked from spawning between waves
* Masking improved on tall tower, short gun platform, and gun wheel 
    * (sneaky off white regions replaced with ffffff pure white)

(Pre Github)

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


### 2/28/2025

* Missile movement climb/dive, variance
* Plane shoots
* Diverse collision tree
* Bio, Blaster, Shock Shield added
* collision tree improved
* Powerups added
* Powerup collision results
* Initial game status text bars


