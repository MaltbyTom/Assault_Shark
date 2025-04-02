# Written by Tom Maltby, (c)Tom Maltby 2025, credits follow
# www.maltby.org
# 
# Currently 2298 lines and a 2213 line dictionary
# Original game: 1521 lines, 1 weekend of coding + 6 hrs resource housekeeping & trim
# 
# Originally based off Jon Fincher's 120 line tutorial py_tut_with_images.py
# py_tut_with_images on github: https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py
# Jon's blog: https://realpython.com/pygame-a-primer/
#
# Additional sounds from  http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
# # Arcade font from https://www.dafont.com/arcade-ya.font , by Yuji Adachi, listed as 100% free
#
# Barring 2 hours last summer, this is my first Python coding, and my first significant coding in any language
# in the last 15 years.  I'm sure it could be more elegant, but I'm having fun.
#
# Thanks to Jon Fincher, and the creators of the great sounds and music
# Graphics except jet, missile, and white cloud are by me, using Corel and Gimp
#
# Joystick handling imported under MIT license:
#  Copyright (c) 2017 Jon Cooper
#
#  pygame-xbox360controller.
#  Documentation, related files, and licensing can be found at
#
#      <https://github.com/joncoop/pygame-xbox360controller>.
#  Thanks to Jon Cooper, simpler than reinventing the wheel
# 
#  The screeninfo module is by authors = ["Marcin Kurczewski <rr-@sakuya.pl>"]
#  The github is at "https://github.com/rr-/screeninfo", the license is MIT, again many thanks!

# Import the pygame module
# Import random for random numbers
# Import os for file handling
# Import tkinter for root graphic context
# Import math for reasons
# Import glob for image preload
# Import controller driver

import random
import pygame
import tkinter
import os
import os.path
import math
import glob
from screeninfo import get_monitors
import xbox360_controller
import edict # Enemy dictionary module
import boxi # Box making module
# Import mouse
import pygame.mouse
#from pygame._sdl2.video import Window

#window = None


#def move(Win):
#    global window
#    window = Win.from_display_module()
#    if window.position[0] == screen_positions [0][0] and window.position[1] == screen_positions[0][1]:
#        window.position = (screen_positions[1][0], screen_positions[1][1])
#    else:
#        window.position = (screen_positions[0][0], screen_positions[0][1])

    #window.position = (0, 32)






# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    K_ESCAPE, #Quit
    K_DOWN,   #Steering
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_SPACE,  #MG
    K_x,  #Flamer
    K_c,  #shock shield
    K_v,  #pulsar
    K_b,  #bio blaster
    K_RETURN,  #Start game
    K_q,
    K_p,  #pause
    K_F1, #help
    KEYDOWN,
    QUIT,
    RLEACCEL,
    K_F5,
    K_RCTRL, #tilt
    K_m,
    K_LCTRL,
    K_l,
    K_s,
    MOUSEBUTTONDOWN,
    MOUSEWHEEL,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)



# Define Colors
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")
LIGHTBLUE = pygame.Color("lightblue1")
DKGRAY = pygame.Color("dimgray")
DKGREEN = pygame.Color("darkgreen")


screen_nums = []
screen_positions = []
screen_sizes = []

def getscreensandsizes():
    screen_num = 0
    for m in get_monitors():
        
        print(str(m))
        # Access individual attributes
        print(f"Monitor name: {m.name}")
        print(f"Position: x={m.x}, y={m.y}")
        #print type({m.x})
        print(f"Size: width={m.width}, height={m.height}")
        print(f"Is primary: {m.is_primary}")
        screen_nums.append(screen_num)
        screen_positions.append((m.x,m.y))
        screen_sizes.append((m.width,m.height))
        screen_num += 1
    #for screen_num in range(screen_count):
        # Create a temporary window for each screen
        #temp_root = tkinter.Toplevel(root)
        #temp_root.withdraw()

        # Get screen width and height
        #width = temp_root.winfo_screenwidth()
        #height = temp_root.winfo_screenheight()

        # Store screen size
        #screen_nums.append(screen_num)
        #screen_sizes.append((screen_num, width, height))

        # Destroy the temporary window
        #temp_root.destroy()
    #root.deiconify()
    return m

# Define constants for the screen width and height
root = tkinter.Tk()
scnums = getscreensandsizes()

SCREEN_WIDTH = int(screen_sizes[0][0])  #root.winfo_screenwidth() # - 50
SCREEN_HEIGHT = int(screen_sizes[0][1])   #root.winfo_screenheight() # - 100
SCREEN_HEIGHT_NOBOX = SCREEN_HEIGHT - 100
boxi.screensetup(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT_NOBOX)

# Define the Sun and Moon object
class SunMoon(pygame.sprite.Sprite):
    def __init__(self, wavenum):
        super(SunMoon, self).__init__()
        # Start with Sun loaded
        self.surf = get_image("sun1.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        # Place randomly
        self.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)

    def update(self, wavenum):

        if wavenum < 3:
            # Keep sun until wave 3
            self.surf = get_image("sun1.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if wavenum > 2 and wavenum < 4:
            # Then replace it with moon
            self.surf = get_image("moon1.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)

# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, firebullet):
        super(Player, self).__init__()
        self.surf = get_image("jet.png")
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        # Start jet in middle of left edge
        self.rect.top = SCREEN_HEIGHT_NOBOX / 2
        self.rect.left = 30
        self.firebullet = 0
        self.hp = 100
        self.armor = 50

    # Move the sprite based on joystick
    #def updatestk(self, )
    jetupdown = 1
    tilt = 1
    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        global buttons
        global jetupdown
        global tilt
        joytilt = False
        if redflash == False and greenflash == False:
            jetupdown = 1
            tilt = 1
            # handle joysticks
            if nojoy == False:
                left_x, left_y = controller.get_left_stick()
                # player move   
                self.rect.move_ip(int(left_x * 5), 0)
                if left_y > .2:
                    jetupdown = 2
                elif left_y < -.2:
                    jetupdown = 0
                else:
                    jetupdown = 1
                self.rect.move_ip(0, int(left_y * 5))
                triggers = controller.get_triggers()
                buttons = controller.get_buttons()
                if triggers > 0.3:
                    self.firebullet = 3
                if buttons[0] == 1:
                    self.firebullet = 4
                if buttons[2] == 1:
                    self.firebullet = 5
                if buttons[1] == 1:
                    self.firebullet = 6
                if buttons[3] == 1:
                    self.firebullet = 7
                if buttons[4] == 1:
                    joytilt = True
                    if jetupdown == 0:
                        self.surf = get_image("jetup.png")
                    elif jetupdown == 1:
                        self.surf = get_image("jet.png")
                    elif jetupdown == 2:
                        self.surf = get_image("jetdown.png")
                    tilt = jetupdown
                else:
                    self.surf = get_image("jet.png")
                self.surf.set_colorkey(WHITE, RLEACCEL)
            
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
                jetupdown = 0
            elif pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
                jetupdown = 2
                move_down_sound.play()
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
            if pressed_keys[K_SPACE]:
                #machine gun
                #shoot_sound.play()
                self.firebullet = 3
            if pressed_keys[K_x]:
                #flamer
                self.firebullet = 4
            if pressed_keys[K_c]:
                #lightning shield
                self.firebullet = 5
            if pressed_keys[K_b]:
                #bioweapon
                self.firebullet = 6
            if pressed_keys[K_v]:
                #pulse
                self.firebullet = 7
            if pressed_keys[K_RCTRL]:
                if jetupdown == 0:
                    self.surf = get_image("jetup.png")
                elif jetupdown == 1:
                    self.surf = get_image("jet.png")
                elif jetupdown == 2:
                    self.surf = get_image("jetdown.png")
                tilt = jetupdown
            else:
                if joytilt == False:
                    self.surf = get_image("jet.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # Keep player on the screen if not on flash       
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT_NOBOX:
                self.rect.bottom = SCREEN_HEIGHT_NOBOX
            
        return(self)                
rbuttimer = 0
portalaniticks = 0
portalctr = 0
gatehouse = False
portal = False
offset = 0

# Define the mountain object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Mountain(pygame.sprite.Sprite):
    def __init__(self):
        global gatehouse
        global portal
        global portalaniticks
        global portalctr
        global offset
        super(Mountain, self).__init__()
        if gatehouse == False:
            if wave < 3:
                self.mountnum = str(random.randint(1,2))
            elif wave < 5:
                self.mountnum = str(random.randint(1,4))
            else:
            #if 1 == 1:
                self.mountnum = str(random.randint(1,6))
                if int(self.mountnum) > 4:
                    if random.randint(1,2) == 2:
                        gatehouse = True
                        if random.randint(1,2) == 2:
                            portal = True
                        # Create the new gatehouse, and add it to our sprite groups
                        offset = 160
                        new_mountain = Mountain()
                        mountains.add(new_mountain)
                        all_sprites.add(new_mountain)            
            self.surf = get_image("mountain" + self.mountnum + ".png")
            self.name = "mountain" + self.mountnum + ".png"
        else:
            if portal == True:                
                self.surf = get_image("gatehousewarp.png")
                self.name = "portal" + str(portalctr) + ".png"
                portalctr += 1
                
            else:
                self.surf = get_image("gatehouseclosed.png")
                self.name = "gatehouse" + str(portalctr) + ".png"
                portalctr += 1
                   
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # Starts on the bottom, off the screen to the right
        self.rect = self.surf.get_rect(bottomleft=(SCREEN_WIDTH + 210 - offset, SCREEN_HEIGHT_NOBOX),)
        offset = 0
        portal = False
        gatehouse = False
        if (random.randint(1,100) + (wave * wave)) > 90: 
                # Spawn gun on rock, more likely in later waves
                new_enemy = Enemy("e_g_cannon7",14,1,self)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # Move the mountain based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        global portalaniticks
        self.rect.move_ip(-5, 0)
        # if off left edge, kill
        if self.name.startswith("portal"):
            portalaniticks += 1
            if portalaniticks == 3:
                self.surf = get_image("gatehousewarpa.png")
                self.surf.set_colorkey(WHITE, RLEACCEL)
            if portalaniticks == 6:
                self.surf = get_image("gatehousewarp.png")
                self.surf.set_colorkey(WHITE, RLEACCEL)
                portalaniticks = 0
        if self.rect.right < 0:
            self.kill()


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):

    def __init__(self, etype, boomcounter, egg, launcher):
        super(Enemy, self).__init__()
        self.name = "enemy" + edict.enemydict[etype]["imgname"]
        self.surf = get_image(edict.enemydict[etype]["imgname"])
        self.surf.set_colorkey(edict.enemydict[etype]["mask"], RLEACCEL) 
        # Random speed, climb/dive   
                    
        if edict.enemydict[etype]["randspeed"]:
            self.speed = random.randint(*edict.enemydict[etype]["speed"])
        else:
            self.speed = edict.enemydict[etype]["speed"]
        if egg == -1:
            eggy = launcher.rect.bottom + random.randint(15,25)
            if eggy >= SCREEN_HEIGHT_NOBOX:
                eggy = SCREEN_HEIGHT_NOBOX - 20
            eggx = launcher.rect.right + random.randint(15,25)
            if eggx >= SCREEN_WIDTH:
                eggx = SCREEN_WIDTH - 20
            self.rect = self.surf.get_rect(center =(eggx,eggy))
        elif edict.enemydict[etype]["randcenter"]:
            if etype.startswith("e_pu"):
                self.rect = self.surf.get_rect(center = (random.randint(edict.enemydict[etype]["centerwidth"][0], edict.enemydict[etype]["centerwidth"][1]), random.randint(edict.enemydict[etype]["centerheight"][0], edict.enemydict[etype]["centerheight"][1])))
            else:
                # Random Center modifies base random positions of (SCREEN_WIDTH, SCREENWIDTH + 20) and (0, SCREEN_HEIGHT_NOBOX)
                self.rect = self.surf.get_rect(center = (random.randint(edict.enemydict[etype]["centerwidth"][0] + SCREEN_WIDTH, edict.enemydict[etype]["centerwidth"][1] + SCREEN_WIDTH + 20), random.randint(edict.enemydict[etype]["centerheight"][0] + 0, edict.enemydict[etype]["centerheight"][1] + SCREEN_HEIGHT_NOBOX )))
        else:
            if edict.enemydict[etype]["islauncher"]:
                randadd = 0
                # Let boss shoot at multiple levels
                if hasattr(launcher, "etype"):
                    if edict.enemydict[launcher.etype]["boss"] == 1:
                        if etype == "e_tent_tentacle91":
                            self.rect = self.surf.get_rect(center=(launcher.rect.left + edict.enemydict[etype]["centerwidth"], launcher.rect.top + edict.enemydict[etype]["centerheight"]))
                        else:
                            randadd = random.randint(-100,100)
                            self.rect = self.surf.get_rect(center=(launcher.rect.left + edict.enemydict[etype]["centerwidth"], launcher.rect.top + randadd + edict.enemydict[etype]["centerheight"]))
                    else:
                        self.rect = self.surf.get_rect(center=(launcher.rect.left + edict.enemydict[etype]["centerwidth"], launcher.rect.top + edict.enemydict[etype]["centerheight"]))    
                else:
                    self.rect = self.surf.get_rect(center=(launcher.rect.left + edict.enemydict[etype]["centerwidth"], launcher.rect.top + edict.enemydict[etype]["centerheight"]))
            else:
                self.rect = self.surf.get_rect(center = (edict.enemydict[etype]["centerwidth"], edict.enemydict[etype]["centerheight"]))               
        if edict.enemydict[etype]["randclimb"]:
            if edict.enemydict[etype]["ishoming"]:
                climbmod = random.randint(*edict.enemydict[etype]["climb"])
                if self.rect.top > player.rect.top:
                    self.climb = - climbmod
                else:
                    self.climb = climbmod
            else:
                self.climb = random.randint(*edict.enemydict[etype]["climb"])
        else:
            self.climb = edict.enemydict[etype]["climb"]
        if edict.enemydict[etype]["isanimated"]:
            self.ticks = edict.enemydict[etype]["ticks"]
        self.fired = edict.enemydict[etype]["fired"]
        self.hp = edict.enemydict[etype]["hp"]

        if edict.enemydict[etype]["boss"]:
            self.basex = SCREEN_WIDTH - 250 + random.randint(-200, 200)
            self.basey = SCREEN_HEIGHT_NOBOX / 2 - self.rect.height / 2 + random.randint(-300, 100)
        
        self.etype = etype
        # set blowup time to enemy as passed
        self.boomcounter = boomcounter
        #if etype == 91:

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        #if self.etype == 91:
        if random.randint(1,10)>5:
            # 50% modify climb if applicable
            if edict.enemydict[self.etype]["randclimb"]:
                # get mod/turn as tuple of random parameters
                climbmod = random.randint(*edict.enemydict[self.etype]["climb"])
                if edict.enemydict[self.etype]["ishoming"]:
                    if self.rect.top > player.rect.top:
                        self.climb = self.climb - climbmod
                    else:
                        self.climb = self.climb + climbmod 
                else:
                    self.climb = self.climb + climbmod
                if edict.enemydict[self.etype]["climbmin"] > self.climb:
                    self.climb = edict.enemydict[self.etype]["climbmin"] 
                if edict.enemydict[self.etype]["climbmax"] < self.climb:
                    self.climb = edict.enemydict[self.etype]["climbmax"]
        if edict.enemydict[self.etype]["isanimated"]:
            # animate through dictionary checks
            #if self.etype == 91:
            framecheck = 0
            gotframe = False
            self.ticks = self.ticks -1
            if self.ticks < 1:
                self.ticks = self.ticks = edict.enemydict[self.etype]["ticks"]
            while gotframe == False:
                if self.ticks > edict.enemydict[self.etype]["aniframetimers"][framecheck]:
                    oldright = self.rect.right
                    oldtop = self.rect.top
                    oldbottom = self.rect.bottom
                    nextimg = edict.enemydict[self.etype]["aniframes"][framecheck]
                    self.surf = get_image(edict.enemydict[self.etype]["aniframes"][framecheck])
                    gotframe = True
                else:
                    framecheck = framecheck + 1
            if self.ticks < 0:
                self.ticks = self.ticks = edict.enemydict[self.etype]["ticks"]
            daboss = None
            if self.etype == "e_tent_tentacle91":
                for e in enemies:
                    if edict.enemydict[e.etype]["boss"]:
                        daboss = e
                if daboss:
                    self.rect = self.surf.get_rect()
                    self.rect.right = daboss.rect.left + 30
                    if nextimg == "tentacledown.png":
                        self.rect.top = daboss.rect.bottom - 60
                    elif nextimg == "tentacleup.png":
                        self.rect.bottom = daboss.rect.bottom - 60
                    elif nextimg == "tentacle.png":
                        self.rect.centery = daboss.rect.bottom - 60
                    else:
                        self.rect.centery = daboss.rect.bottom - 50
                else:
                    self.kill()
                    return
            self.surf.set_colorkey(edict.enemydict[self.etype]["mask"], RLEACCEL)

        # Move the enemy
        if edict.enemydict[self.etype]["advancedmovement"] == True:
            #if self.etype == 91:
            isdone = amove(self) 
        #for e in enemies:
            #if e.etype == 91:
        if hasattr(self, "rect"):
            if hasattr(self.rect, "move_ip"):
                self.rect.move_ip(-self.speed, self.climb)
                # Kill it if offscreen
                if self.rect.right < 0:
                    self.kill()
                if self.rect.left > SCREEN_WIDTH + 100:
                    self.kill()
                # Make top & bottom permeable to powerups; other enemies must stay in screen
                if self.rect.bottom > SCREEN_HEIGHT_NOBOX:
                    # ENEMY GROUND COLLISIONS
                    if edict.enemydict[self.etype]["ispowerup"] == False:
                        if edict.enemydict[self.etype]["isground"] == False: # Missile Launcher should be on ground
                            # Otherwise Don't leave
                            self.rect.bottom = SCREEN_HEIGHT_NOBOX - 50
                            # Bounce
                            self.climb = self.climb * - 1 # * self.climb
                        if edict.enemydict[self.etype]["damground"] > 0:
                            self.hp = self.hp - int(100 * (edict.enemydict[self.etype]["damground"]/100))
                            if self.hp < 0:
                                # Explode missiles, blimps
                                if edict.enemydict[self.etype]["isexplodable"]:
                                    self.etype = edict.enemydict[self.etype]["isexplodable"]
                                else:
                                    if edict.enemydict[self.etype]["isexploded"] == False:
                                        self.kill()
                if self.rect.top < 0:
                    if edict.enemydict[self.etype]["ispowerup"] == False:
                        # Don't leave
                        self.top = 5
                        # Bounce
                        self.climb = 3
                    elif self.rect.bottom < 0: # But don't let them disappear up without cleanup
                        self.kill()
        if edict.enemydict[self.etype]["islayer"] == True:
            if random.randint(1,100) > 98:
                if redflash == False and greenflash == False:
                    new_enemy = Enemy(edict.enemydict[self.etype]["eggtype"],14,-1,self)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
        if edict.enemydict[self.etype]["isshooter"] == True:   
            # Functional blimp or missile launcher or cannon, potentialy etc
            if redflash == False:
                if random.randint(1,100) + wave * 2 > 90 and self.fired == 0:
                    # Shoot designated ammotype
                    if edict.enemydict[self.etype]["boss"]:
                        if tentacleattack == False:
                            possibles = len(edict.enemydict[self.etype]["ammotype"]) - 1
                            shot = edict.enemydict[self.etype]["ammotype"][random.randint(0, possibles)]
                            new_enemy = Enemy(shot,14,1,self)
                    else:    
                        new_enemy = Enemy(edict.enemydict[self.etype]["ammotype"],14,1,self)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                    self.fired = edict.enemydict[self.etype]["fired"]
                elif self.fired > 0:
                    self.fired = self.fired - 1
        if edict.enemydict[self.etype]["isexploded"]: # or           
            self.hp = 1
            # Exploding animation            
            self.boomcounter -= 1
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill()
            framecheck = 0
            gotframe = False
            while gotframe == False and self.boomcounter > 0:
                if self.boomcounter > edict.enemydict[self.etype]["expframetimers"][framecheck]:
                    self.surf = get_image(edict.enemydict[self.etype]["expframes"][framecheck])
                    gotframe = True
                else:
                    framecheck = framecheck + 1
            self.surf.set_colorkey(edict.enemydict[self.etype]["mask"], RLEACCEL)
        # Hatching routine
        if self.etype.startswith("e_egg"):
            self.boomcounter -= 1
            if self.boomcounter < 1:
                if edict.enemydict[self.etype]["isexplodable"]:
                    self.etype = edict.enemydict[self.etype]["isexplodable"]
                    self.speed = edict.enemydict[self.etype]["speed"][0]
        
        if edict.enemydict[self.etype]["skyburst"]:  #self.etype == 81: # Cannon shell
            # Don't let off screen
            if self.rect.right < 0:
                self.kill
            if random.randint(1,10) == 10:
                # Slow climb gradually but randomly
                self.climb = self.climb + 1
            if self.rect.bottom > SCREEN_HEIGHT_NOBOX or self.rect.top < 0:
                # Kill at top/bottom
                self.kill
            if self.climb > -1:
                # Detonate at peak of arc
                if edict.enemydict[self.etype]["isexplodable"]:
                    self.etype = edict.enemydict[self.etype]["isexplodable"]
                    self.boomcounter = 7 # Abbreviated explosion
                else:
                    self.kill()
        if edict.enemydict[self.etype]["isground"] == True:
            self.rect.bottom = SCREEN_HEIGHT_NOBOX
        #for e in enemies:
        #    if e.etype == 91:

# Define the bullet object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self,startx,starty,btype,boomcounter):
        super(Bullet, self).__init__()
        global tilt
        self.btype = btype
        # Apply machine gun upgrades
        if btype == 1:
            if mgtype == 1:
                self.surf = get_image("bullet.png")
            if mgtype == 2:
                self.surf = get_image("bullet2.png")
            if mgtype == 3:
                self.surf = get_image("bullet3.png")
        else:
            self.surf = get_image(bulletdict[self.btype]["imgname"])
        self.name = "bullet" + bulletdict[self.btype]["imgname"]
        self.speed = bulletdict[self.btype]["bspeed"]
        bulletdict[self.btype]["sound"].play()
        self.boomcounter = boomcounter
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # The starting position is the nose of the plane
        self.rect = self.surf.get_rect(center = (startx, starty))
        match tilt:
            case 0:
                self.climb = -15
            case 1:
                self.climb = 0
            case 2:                
                self.climb = 15
        # Adjust climb for outside bullets on multibullet
        match boomcounter:
            case 9:
                self.climb += 1
            case 11:
                self.climb += 2
            case 10:
                self.climb -= 1
            case 12:
                self.climb -= 2
            case 13:
                # Spawned as rebound
                self.rect.bottom = SCREEN_HEIGHT_NOBOX - 5
                self.speed = bounceinherits + 2
                self.climb = bounceinheritc
            case 14:
                # Spawned as second rebound
                self.rect.bottom = SCREEN_HEIGHT_NOBOX - 5
                self.speed = bounceinherits + 4
                self.climb = bounceinheritc
        
    # Move the bullet based on speed
    # Remove it when it passes the right edge of the screen
    def update(self):
        global bounceinheritc
        global bounceinherits
        self.rect.move_ip(self.speed, self.climb)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        # Check for bouncing or bounce/multiplying MG ammo upgrades if bullet hits ground
        if self.rect.top > SCREEN_HEIGHT_NOBOX:
            if self.btype == 1:
                match mgbounce:
                    case 0:
                        self.kill()
                    case 1:
                        self.climb = self.climb * -1
                        self.rect.bottom = SCREEN_HEIGHT_NOBOX - 5
                        # bounce
                    case 2:
                        self.climb = self.climb * -1
                        self.rect.bottom = SCREEN_HEIGHT_NOBOX - 5
                        # bounce 2 bullets
                        bounceinherits = self.speed
                        bounceinheritc = self.climb
                        new_bullet = Bullet(self.rect.right, self.rect.top, 1, 13)                        
                        bullets.add(new_bullet)
                        all_sprites.add(new_bullet)
                    case 3:
                        self.climb = self.climb * -1
                        self.rect.bottom = SCREEN_HEIGHT_NOBOX - 5
                        # bounce 3 bullets
                        bounceinherits = self.speed
                        bounceinheritc = self.climb
                        new_bullet = Bullet(self.rect.right, self.rect.top, 1, 13)                        
                        bullets.add(new_bullet)
                        all_sprites.add(new_bullet)
                        new_bullet = Bullet(self.rect.right, self.rect.top, 1, 14)                        
                        bullets.add(new_bullet)
                        all_sprites.add(new_bullet)
            else:  
                self.kill()
        if self.btype == 1:
            if pygame.sprite.spritecollideany(self, mountains):
                self.kill()
        if bulletdict[self.btype]["isanimated"]:
            self.boomcounter = self.boomcounter - 1
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill()
            framecheck = 0
            gotframe = False
            while gotframe == False and self.boomcounter > 0:
                if self.boomcounter > bulletdict[self.btype]["frametimers"][framecheck]:
                    self.surf = get_image(bulletdict[self.btype]["frames"][framecheck])
                    gotframe = True
                else:
                    framecheck = framecheck + 1
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # Shock Lances from active shock shield
            if bulletdict[self.btype]["shield"] == True:
                self.rect.centerx = player.rect.centerx + random.randint(-3, 3)
                self.rect.centery = player.rect.centery + random.randint(-3, 3)
                # This is a Shock Lance spawner to increase the effect and wow-factor of the shock shield
                pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
                if enemies:
                    # If there aren't already bushels of Shock Lances flying around
                    if len(bullets) < 100:
                        closeenemies = []
                        for e, enem in enumerate(enemies):
                            chkdist = pos.distance_to(pygame.math.Vector2(enem.rect.centerx, enem.rect.centery))
                            if chkdist < 300:
                                # Gather a list of enemies within 300 of player
                                closeenemies.append(enem)
                        # If there are enemies closer than 300
                        if len(closeenemies) > 0:
                            # Throw shock bolts from the shock shield at nearby enemies
                            for e in closeenemies:
                                edist = pos.distance_to(pygame.math.Vector2(e.rect.centerx, e.rect.centery))
                                if edist < 300:
                                    new_bullet = Bullet(player.rect.centery,player.rect.centerx,6,3)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    yoffset = e.rect.centery - player.rect.centery
                                    xoffset = e.rect.centerx - player.rect.centerx
                                    rotation = math.degrees(math.atan2(yoffset, xoffset))
                                    scalesurf = pygame.transform.scale(new_bullet.surf, (new_bullet.rect.height, edist))
                                    finsurf = pygame.transform.rotate(scalesurf, rotation)
                                    new_bullet.surf = finsurf
                                    new_bullet.rect = new_bullet.surf.get_rect()
                                    if e.rect.centery < player.rect.centery:
                                        new_bullet.rect.bottomleft = player.rect.center
                                    else:
                                        new_bullet.rect.topleft = player.rect.center

            if self.btype == 6:
                # Shock Lance
                self.rect.centerx = player.rect.centerx + random.randint(-3, 3)
                self.rect.centery = player.rect.centery + random.randint(-3, 3)
                pos = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
                if enemies:
                    closestenemy = min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.centerx, e.rect.centery)))
                    edist = pos.distance_to(pygame.math.Vector2(closestenemy.rect.centerx, closestenemy.rect.centery))
                    if edist < 300:
                        yoffset = closestenemy.rect.centery - player.rect.centery
                        xoffset = closestenemy.rect.centerx - player.rect.centerx
                        # This extra rotation / scale started as an error, but is just the spectacular touch we needed
                        # The scaling of an already rotated sprite causes spectacular and chaotic 'jumping the gap'
                        rotation = math.degrees(math.atan2(yoffset, xoffset))
                        scalesurf = pygame.transform.scale(self.surf, (self.rect.height, edist))
                        finsurf = pygame.transform.rotate(scalesurf, rotation)
                        self.surf = finsurf
                        self.surf.set_colorkey(WHITE, RLEACCEL)
                        self.rect = self.surf.get_rect()
                        self.rect.center = closestenemy.rect.center
                        
                
        if self:
            center = self.rect.center
            self.rect = self.surf.get_rect()
            self.rect.center = center   

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Cloud, self).__init__()
        if "bling" in kwargs:
            self.surf = kwargs["bling"]
            self.surf.set_colorkey(WHITE, RLEACCEL)
            self.rect = self.surf.get_rect()
            self.rect.center = kwargs["location"]
            self.number = True
            self.duration = 25
            self.climb = random.randint(-25, -10)
            self.travel = random.randint(-10, 10)
            #self.loc = kwargs["location"]
            # The starting position is player location
            #self.rect = self.surf.get_rect(center=(self.loc[0],self.loc[1],))
            #print("made at ")
        else:
            self.number = None
            if wave < 3:
                # During the day, use light clouds
                #self.surf = edict.red16nums[50]
                self.surf = get_image("cloud.png")
            else:
                # At night, use dark clouds
                self.surf = get_image("cloud2.png")
            
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # The starting position is randomly generated
            self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT_NOBOX - 200),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        #print(self.number)
        if hasattr(self, "number"):
            if self.number == True:
                #print("moving")
                up = self.climb
                self.climb += 2
                side = self.travel
                self.rect.move_ip(side, up)
                self.duration -= 1
                if self.duration < 1:
                        self.kill()
            else:
                self.rect.move_ip(-6, 0)
                # if off left edge, kill
                if self.rect.right < 0:
                    self.kill()   

# Advanced movement function(s)

def amove(thise):
    if thise.etype == "e_tent_tentacle91":
        # Tentacle
        #daboss = False
        for e in enemies:
            if edict.enemydict[e.etype]["boss"] == True:
                daboss = e
        #if daboss:
            
            #if edict.enemydict[daboss]["isexploded"]:
            #    thise.kill()
            #thise.rect.right = daboss.rect.left + 25
            #if thise.ticks == 1:
            #    thise.kill()
            #elif thise.ticks < 15 or thise.ticks > 19 or thise.ticks == 17 or thise.ticks == 18:
            #    thise.rect.centery = daboss.rect.bottom - 50
            #elif thise.ticks == 15 or thise.ticks == 16:
            #    thise.rect.bottom = daboss.rect.bottom - 70
            #elif thise.ticks == 19 or thise.ticks == 20:
            #    thise.rect.top == daboss.rect.bottom - 70
       # else:
        #    thise.kill()
    else:
        # right now,  only the boss
        # For the first case, assume a desire to stay in the vertical center, 150 pixels from the back edge of the screen
        # Initialize locals
        if edict.enemydict[thise.etype]["boss"]:
            movex = 0
            movey = 0
            # Set base coordinates
            basey = thise.basey
            basex = thise.basex
            # establish proposed move
        
            if player.rect.right + 500 > thise.rect.left:
                if player.rect.top > thise.rect.bottom:
                    # Dive
                    thise.climb = 6
                elif player.rect.bottom < thise.rect.top + 75:
                    # Climb
                    thise.climb = - 6
                if player.rect.right + 300 > thise.rect.left:
                    if player.rect.right > thise.rect.right:
                        thise.speed = -5
                    elif player.rect.bottom > thise.rect.top + 75:
                        if player.rect.top < thise.rect.bottom:
                            # Tentacle attack
                            tentacleattack = False
                            for e in enemies:
                                if e.etype == "e_tent_tentacle91":
                                    tentacleattack = True
                            if tentacleattack == False:
                                tentacleattack = True
                                new_enemy = Enemy("e_tent_tentacle91",14,300,thise)
                                enemies.add(new_enemy)
                                all_sprites.add(new_enemy)
                else:
                    thise.speed = 8
                    # Charge 
            else:
                movey = thise.climb + thise.rect.bottom
                if thise.speed > 5:
                    movex = thise.speed + thise.rect.left
                else:
                    movex = thise.speed + thise.rect.right
                # Adjust towards base on probablility of distance per axis
                if movex > basex:
                    percreturn = movex - basex
                    if random.randint(1,100) < percreturn:
                        thise.speed = thise.speed + 3
                if movex < basex:
                    percreturn = (basex - movex) // 5        
                    if random.randint(1,100) < percreturn:
                        thise.speed = thise.speed - 3
                
                # Update proposed x position
                if thise.speed > 5:
                    movex = thise.speed + thise.rect.left
                else:
                    movex = thise.speed + thise.rect.right
                if movey > basey:
                    percreturn = (movey - basey) // 2
                    if random.randint(1,100) < percreturn:
                        thise.climb = thise.climb - 3
                if movey < basey:
                    percreturn = basey - movey        
                    if random.randint(1,100) < percreturn:
                        thise.speed = thise.speed + 3
                # Update proposed y position
                movey = thise.climb + thise.rect.bottom
                # Now check that we aren't running into another boss, a mountain or the ground
                if movey > SCREEN_HEIGHT_NOBOX:
                    movey = SCREEN_HEIGHT_NOBOX - 50
            
            movey = thise.climb + thise.rect.bottom
            if thise.speed > 5:
                movex = thise.speed + thise.rect.left
            else:
                movex = thise.speed + thise.rect.right
            for e in enemies:
                if e.rect.collidepoint(movex, movey):
                    if e is not thise:
                        if edict.enemydict[e.etype]["boss"]:
                            if e.rect.left > thise.rect.left:
                                e.rect.left += 10
                                thise.speed = -5
                                e.speed = 5
                            else:
                                thise.speed = 5
                                e.speed = -5
                                e.rect.left -= 10
                            if e.rect.top > thise.rect.top:
                                thise.climb = -5
                                e.climb = 5
                                e.rect.top += 10
                            else:
                                thise.climb = 5
                                e.climb = -5
                                e.rect.top -= 10
            if len(mountains) > 0:
                for m in mountains:
                    if m.rect.collidepoint(movex, movey):
                        thise.climb = -5
                        thise.speed = 5

            # Don't chase past half screen
            if thise.rect.left < SCREEN_WIDTH / 2:
                thise.rect.left = SCREEN_WIDTH / 2
                thise.speed = -5
            # Don't leave the screen
            
            if thise.rect.right > SCREEN_WIDTH:
                thise.rect.right = SCREEN_WIDTH - 30
                thise.speed = 6
            if thise.rect.left < 0:
                thise.rect.left = 30
                thise.speed = -6
            if thise.rect.top < 0:
                thise.rect.top = 30
                thise.climb = -3
            if thise.rect.bottom > SCREEN_HEIGHT_NOBOX:
                thise.rect.bottom = SCREEN_HEIGHT_NOBOX - 50
                thise.climb = + 3
            if thise.speed > 15:
                thise.speed = 15
            if thise.speed < -15:
                thise.speed = -15
            if thise.climb > 8:
                thise.climb = 8
            if thise.climb < -8:
                thise.climb = -8
        #for e in enemies:
            #if e.etype == 91: 
        return(thise)
    


# Define and cache fonts

pygame.font.init()
font8 = pygame.font.Font("fonts/arcade_r.ttf", 8)
font10 = pygame.font.Font("fonts/arcade_r.ttf", 10)
font12 = pygame.font.Font("fonts/arcade_r.ttf", 12)
font15 = pygame.font.Font("fonts/arcade_r.ttf", 15)
font16 = pygame.font.Font("fonts/arcade_r.ttf", 16)
font20 = pygame.font.Font("fonts/arcade_r.ttf", 20)
font30 = pygame.font.Font("fonts/arcade_r.ttf", 30)
font50 = pygame.font.Font("fonts/arcade_r.ttf", 50)
font60 = pygame.font.Font("fonts/arcade_r.ttf", 60)
font75 = pygame.font.Font("fonts/arcade_r.ttf", 75)

# Cache repeated text renders
playagametextblack = font20.render("Press [Enter]/(Start) To Play - Press [Esc]/(Back) to Quit", 1, BLACK)
playagametextred = font20.render("Press [Enter]/(Start) To Play - Press [Esc]/(Back) to Quit", 1, RED)
pausetext1 = font20.render(" [Keyboard Controls]:", 1, BLACK)
pausetext2 = font16.render("Flying: Arrow keys - [Up], [Down], [Left], [Right] -- Tilt: [R Ctrl]", 1, BLACK)
pausetext3 = font16.render("Weapons: [Space] - Machine Gun, [X] - Flamer, [C] - Shock Shield, [V] - Pulsar, [B] - Bio Blast", 1, BLACK)
pausetext4 = font16.render("[Enter] - Play / Pause / Unpause, [Escape] - Quit ", 1, BLACK)
pausetext5 = font20.render("Press [Enter] To UnPause - Press [Esc] to Quit", 1, BLACK)
pausetext1red = font20.render(" [Keyboard Controls]:", 1, RED)
pausetext2red = font16.render("Flying: Arrow keys - [Up], [Down], [Left], [Right] -- Tilt: [R Ctrl]", 1, RED)
pausetext3red = font16.render("Weapons: [Space] - Machine Gun, [X] - Flamer, [C] - Shock Shield, [V] - Pulsar, [B] - Bio Blast", 1, RED)
pausetext4red = font16.render("[Enter] - Play / Pause / Unpause, [Escape] - Quit ", 1, RED)
pausetext5red = font20.render("Press [Enter] To UnPause - Press [Esc] to Quit", 1, RED)
pausetext6 = font20.render(" (Joystick Controls):", 1, BLACK)
pausetext7 = font16.render("Flying: Left Stick - (Up), (Down), (Left), (Right) -- Tilt: (Left Bump Trigger)", 1, BLACK)
pausetext8 = font16.render("Weapons: (Right Trigger) - Machine Gun, (A) - Flamer, (X) - Shock Shield, (B) - Pulsar, (Y) - Bio Blast", 1, BLACK)
pausetext9 = font16.render("(Start) - Play / Pause / Unpause, (Back) - Quit ", 1, BLACK)
pausetext10 = font20.render("Press (Start) To UnPause - Press (Back) to Quit", 1, BLACK)
pausetext6red = font20.render(" (Joystick Controls):", 1, RED)
pausetext7red = font16.render("Flying: Left Stick - (Up), (Down), (Left), (Right) -- Tilt: (Left Bump Trigger)", 1, RED)
pausetext8red = font16.render("Weapons: (Right Trigger) - Machine Gun, (A) - Flamer, (X) - Shock Shield, (B) - Pulsar, (Y) - Bio Blast", 1, RED)
pausetext9red = font16.render("(Start) - Play / Pause / Unpause, (Back) - Quit ", 1, RED)
pausetext10red = font20.render("Press (Start) To UnPause - Press (Back) to Quit", 1, RED)
vaulttext1red = font16.render("This vault is long abandoned.  It's doors are blocked by fallen rock.", 1 , RED)
vaulttext2red = font16.render("If only you had tools to move the debris and a repair kit to fix the hyperlink!", 1, RED)
vaulttext3red = font20.render("Press [Enter]/(Start) to leave the vault!", 1, RED)
vaulttext4red = font16.render("Working with the biokit on your assault shark, you manage to restore some of the cryogenic cloning hangars.", 1, RED)
vaulttext5red = font20.render("Press [SPACE] on keyboard or (A) on controller to set/update savepoint.", 1, RED)
vaulttext6red = font20.render("Save point set!", 1, RED)
loadasktextred = font16.render("A cloned assaultshark is available in the cryo-labs!  Press (B) on joystick or [L] on keyboard to restore", 1, RED)
loadedtextred = font16.render("Your cloned ship has been fetched from the cryolabs, restored, and made ready", 1, RED)
setuptextred = font16.render("Press (X) on joystick or [S] on keyboard to set your shark pilot's initials and game settings", 1, RED)
loadtextred = font16.render("Arrow keys or left stick select.  Press (A) on joystick or [ENTER] on keyboard to load selected game.", 1, RED)
settextred = font16.render("Arrow keys or left stick select.  Press (A) on joystick or [ENTER] on keyboard to accept settings.", 1, RED)
settextred2 = font16.render("(Y) or [SPACE] randomizes initials.", 1, RED)
loaded = 0

# This generates dictionaries of flyaway numbers in different colors
edict.gennumbers()

def texts(lives, score):
    # gives lives, score, waves, high score
    scoretext=font20.render("Lives:" + str(lives) + "  Score:" + str(score) +"  Wave: " + str(wave)+ ":" + "  (" + str(wavecounter) + "/" + str(wavegoal) + ")" +"   High Score: "+str(highscore), 1, (0,0,0))
    screen.blit(scoretext, (52, SCREEN_HEIGHT - 27))
    scoretext=font20.render("Lives:" + str(lives) + "  Score:" + str(score) +"  Wave: " + str(wave)+ ":" + "  (" + str(wavecounter) + "/" + str(wavegoal) + ")" +"   High Score: "+str(highscore), 1, (0,0,255))
    screen.blit(scoretext, (50, SCREEN_HEIGHT - 25))
    initstext = font30.render("Pilot: " + initials, 1, BLACK)
    screen.blit(initstext, (32, SCREEN_HEIGHT - 87))
    initstext = font30.render("Pilot: " + initials, 1, BLUE)
    screen.blit(initstext, (30, SCREEN_HEIGHT - 85))

def texts2(flamer, shock, bio, pulse):
    # gives ammo - machinegun has infinite ammo
    scoretext=font15.render("MG(SP): 999   FLAMER(X): "+str(flamer)+"  SHOCK SHIELD(C): " + str(shock)  + "  PULSAR(V): " + str(pulse) + "   BIO BLAST(B): "+str(bio), 1, (0,0,0))
    screen.blit(scoretext, (52, SCREEN_HEIGHT - 47))
    scoretext=font15.render("MG(SP): 999   FLAMER(X): "+str(flamer)+"  SHOCK SHIELD(C): "+str(shock) + "  PULSAR(V): " + str(pulse) + "   BIO BLAST(B): "+str(bio), 1, (0,0,255))
    screen.blit(scoretext, (50, SCREEN_HEIGHT - 45))

def texts3(highscore):
    # on enter to play screen, gives high score
    global playscreenupdated
    ptxtoffset = playagametextblack.width / 2
    screen.blit(playagametextblack, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 360))
    screen.blit(playagametextred, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 362))
    playagametext = font60.render("High Score: "+str(highscore), 1, (0,0,0))
    ptxtoffset = playagametext.width / 2
    screen.blit(playagametext, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 200))
    playagametext = font60.render("High Score: "+str(highscore), 1, (255,0,0))
    screen.blit(playagametext, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 202))
    # Control list
    ptxtoffset = pausetext1.width / 2
    screen.blit(pausetext1, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 -355))
    screen.blit(pausetext1red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + -353))
    ptxtoffset = pausetext2.width / 2
    screen.blit(pausetext2, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 330))
    screen.blit(pausetext2red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 328))
    ptxtoffset = pausetext3.width / 2
    screen.blit(pausetext3, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 -310))
    screen.blit(pausetext3red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 -308))
    ptxtoffset = pausetext4.width / 2
    screen.blit(pausetext4, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 290))
    screen.blit(pausetext4red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 -288))
    # Joystick controls
    ptxtoffset = pausetext6.width / 2
    screen.blit(pausetext6, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 240))
    screen.blit(pausetext6red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 238))
    ptxtoffset = pausetext7.width / 2
    screen.blit(pausetext7, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 215))
    screen.blit(pausetext7red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 213))
    ptxtoffset = pausetext8.width / 2
    screen.blit(pausetext8, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 -195))
    screen.blit(pausetext8red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 193))
    ptxtoffset = pausetext9.width / 2
    screen.blit(pausetext9, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 175))
    screen.blit(pausetext9red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 173))
    loaddataexists = edict.loadgame()
    # returns number of saved games
    listsize = edict.loadgame()
    # Add rendered versions of savenames to dictionary
    # Add a dictionary key "render" containing renders of the text keys
    renderedtext = boxi.rendertextdic(edict.savedict, font20, RED)
    if loaddataexists > 0:
        if loaded == 0:
            ptxtoffset = loadasktextred.width / 2
            ptxtlft = SCREEN_WIDTH / 2 - ptxtoffset
            boxi.boxi(screen,loadasktextred,SCREEN_HEIGHT / 2 + 320, ptxtlft, 2, BLACK, 3, RED, 0, 0)
        else:
            ptxtoffset = loadedtextred.width / 2
            ptxtlft = SCREEN_WIDTH / 2 - ptxtoffset
            boxi.boxi(screen,loadedtextred,SCREEN_HEIGHT / 2 + 320, ptxtlft, 2, BLACK, 3, RED, 0, 0) 
    boxi.boxi(screen, setuptextred, SCREEN_HEIGHT / 2 + 275, SCREEN_WIDTH / 2 - setuptextred.width/2, 2, BLACK, 3, RED, 0, 0)
    playscreenupdated = True
    

def texts4():
    global pausescreenupdated
    #Pause screen    
    ptxtoffset = pausetext5.width / 2
    screen.blit(pausetext5, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 30))
    screen.blit(pausetext5red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 28))
    #Control list
    ptxtoffset = pausetext1.width / 2
    screen.blit(pausetext1, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2))
    screen.blit(pausetext1red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 2))
    ptxtoffset = pausetext2.width / 2
    screen.blit(pausetext2, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 20))
    screen.blit(pausetext2red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 22))
    ptxtoffset = pausetext3.width / 2
    screen.blit(pausetext3, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 40))
    screen.blit(pausetext3red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 42))
    ptxtoffset = pausetext4.width / 2
    screen.blit(pausetext4, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 60))
    screen.blit(pausetext4red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 62))
    # Joystick controls
    ptxtoffset = pausetext6.width / 2
    screen.blit(pausetext6, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 185))
    screen.blit(pausetext6red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 183))
    ptxtoffset = pausetext7.width / 2
    screen.blit(pausetext7, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 165))
    screen.blit(pausetext7red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 163))
    ptxtoffset = pausetext8.width / 2
    screen.blit(pausetext8, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 -145))
    screen.blit(pausetext8red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 143))
    ptxtoffset = pausetext9.width / 2
    screen.blit(pausetext9, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 125))
    screen.blit(pausetext9red, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 123))
    pausescreenupdated = True

loadgame = ""
def readgamedict(*args, **kwargs):
    global loaded, loaddataexists
    global plives, score, flamer, shock, bio, pulse, redflash, greenflash, mgmult, mgtype, mgbounce, bounceinheritc, bounceinherits
    global healthmax, armormax, wavecounter, wavegoal, waveboss, waveendticks, jetupdown, tilt, wave, initials

    initsuff = "savepoint"
    if "initsuff" in kwargs:
        initsuff = kwargs["initsuff"]
    wave = edict.savedict[initsuff]["wave"]
    score = edict.savedict[initsuff]["score"]
    ammo = edict.savedict[initsuff]["ammo"]
    flamer = ammo[0]
    shock = ammo[1]
    bio = ammo[2]
    pulse = ammo[3]
    mg  = edict.savedict[initsuff]["mg"]
    mgmult = mg[0]
    mgtype = mg[1]
    mgbounce = mg[2]
    plives = edict.savedict[initsuff]["lives"]
    player.hp = edict.savedict[initsuff]["health"]
    healthmax = edict.savedict[initsuff]["healthmax"]
    player.armor = edict.savedict[initsuff]["armor"]
    armormax = edict.savedict[initsuff]["armormax"] 
    if "initials" in edict.savedict[initsuff]:
        initials = edict.savedict[initsuff]["initials"]

    if wave > 1:
        wavct = 1
        while wavct < wave:
            wavegoal = wavegoal + ((wavct + 1) * (wavct + 1) * 10) + 100
            wavct = wavct + 1

def savegame():
    initsuff = "savepoint" + initials
    asavedict = {}
    ammo = {}
    mg = {}
    asavedict = {initsuff: {"wave": wave}}
    #asavedict[initsuff]["wave"] = wave
    asavedict[initsuff]["score"] = score
    ammo = [flamer, shock, bio, pulse]
    asavedict[initsuff]["ammo"] = ammo
    mg = [mgmult, mgtype, mgbounce]
    asavedict[initsuff]["mg"] = mg
    asavedict[initsuff]["lives"] = plives
    asavedict[initsuff]["health"] = player.hp
    asavedict[initsuff]["healthmax"] = healthmax
    asavedict[initsuff]["armor"] = player.armor
    asavedict[initsuff]["armormax"] = armormax
    asavedict[initsuff]["initials"] = initials
    edict.savegame(asavedict, initsuff)
    return asavedict

# Functions for Boxibuttons:
a1 = 0
a2 = 0
a3 = 0
def randomizebutton():
    global a1
    global a2
    global a3
    a1 = 72 + random.randint(1, 72)
    a2 = 72 + random.randint(1, 72)
    a3 = 72 + random.randint(1, 72)
    # This sets up an animation event for the randomization of the 'AAA' initials style control in the while running loop.
    # The control generates a three character text string, intended for use with high scores and save games.
    # Mostly I stuck this in because I realized that it was the only piece missing from a slot machine style wheel of pictures
    # display - it is fun and cool looking, which are generally good things in a game UI.
def newnumber(number1, loc):
    new_number = Cloud(bling = number1, location = loc)
    clouds.add(new_number)
    all_sprites.add(new_number)

# Animation timers
isanioverflag = True
isaniover = 0

healthhardmax = 400
armorhardmax = 200
healthmax = 200
armormax = 100
bossmode = False
wasbossmode = bossmode
bosshealthblink = 0
# MG POWERUPS
# 1, 2, 3, 5, 7
mgmult = 1
# 1, 2, 3
mgtype = 1
# 0, 1, 2
mgbounce = 0
# x, y, speed, climb
bounceinheritc = 0
bounceinherits = 0

def mgbar(left, top):
    # Initialize Machine Gun Panel images
    # 
    mgbutimg  = get_image("mgbut.png")
    mgbarimg = get_image("mgbar.png")
    ximg = get_image("x.png")
    ximg.set_colorkey(WHITE, RLEACCEL)
    x2img = get_image("x2.png")
    x2img.set_colorkey(WHITE, RLEACCEL)
    x3img = get_image("x3.png")
    x3img.set_colorkey(WHITE, RLEACCEL)
    x5img = get_image("x5.png")
    x5img.set_colorkey(WHITE, RLEACCEL)
    x7img = get_image("x7.png")
    x7img.set_colorkey(WHITE, RLEACCEL)
    b1img = get_image("b1.png")
    b1img.set_colorkey(WHITE, RLEACCEL)
    b2img = get_image("b2.png")
    b2img.set_colorkey(WHITE, RLEACCEL)
    b3img = get_image("b3.png")
    b3img.set_colorkey(WHITE, RLEACCEL)
    ammo1img = get_image("ammo1.png")
    ammo1img.set_colorkey(WHITE, RLEACCEL)
    ammo2img = get_image("ammo2.png")
    ammo2img.set_colorkey(WHITE, RLEACCEL)
    ammo3img = get_image("ammo3.png")
    ammo3img.set_colorkey(WHITE, RLEACCEL)   

    #mgbarimg.blit(freshmgbar,(0,0))
    screen.blit(mgbarimg,(left,top))

    match mgmult:

        case 1:
            screen.blit(ximg,(left,top))
        case 2:
            screen.blit(mgbutimg,(left+1,top+1))
            screen.blit(x2img,(left,top))
        case 3:
            screen.blit(mgbutimg,(left+1,top+1))
            screen.blit(x3img,(left,top))
        case 5:
            screen.blit(mgbutimg,(left+1,top+1))
            screen.blit(x5img,(left,top))
        case 7:
            screen.blit(mgbutimg,(left+1,top+1))
            screen.blit(x7img,(left,top))

    match mgbounce:

        case 0:
            #screen.blit(mgbutimg,(left + 31,top))
            screen.blit(ximg,(left + 31,top))
        case 1:
            screen.blit(mgbutimg,(left + 31,top+1))
            screen.blit(b1img,(left + 31,top))
        case 2:
            screen.blit(mgbutimg,(left + 31,top+1))
            screen.blit(b2img,(left + 31,top))
        case 3:
            screen.blit(mgbutimg,(left + 31,top+1))
            screen.blit(b3img,(left + 31,top))
    
    match mgtype:
        case 1:
            screen.blit(mgbutimg,(left + 61,top + 1))
            screen.blit(ammo1img,(left + 61,top))
        case 2:
            screen.blit(mgbutimg,(left + 61,top+1))
            screen.blit(ammo2img,(left + 61,top))
        case 3:
            screen.blit(mgbutimg,(left + 61,top+1))
            screen.blit(ammo3img,(left + 61,top))            
    
    #mgbarimg.blit(ximg,(31,0))
    #mgbarimg.blit(ximg,(61,0))

def healthbar(left, top, health):
    #if health > healthmax:
    healthbarborder = pygame.Rect(left + 240, top, healthmax, 30)
    healthbarfilled = pygame.Rect(left + 242, top + 2, int((healthmax - 4) * (health/(healthmax/2))), 26)
    heartimg = get_image("heart.png")
    heartimg.set_colorkey(WHITE, RLEACCEL)
    healthbarmark = pygame.Rect(left + 437, top-3, 1, 33)
    if health > 70:
        healthbarcolor = GREEN
    elif health > 30:
        healthbarcolor = YELLOW
    else:
        healthbarcolor = RED
    pygame.draw.rect(screen, BLACK, healthbarborder, 0, 2)
    pygame.draw.rect(screen, healthbarcolor, healthbarfilled, 0, 2)
    if healthmax > 200:
        pygame.draw.rect(screen, BLACK, healthbarmark, 0, 0)
    
    screen.blit(heartimg, (left + 210,top))
    #return health

def bosshealthbar(left, top, boss, health, bosshealthblink):
 
    bhealthmax = edict.enemydict[boss.etype]["hp"] / 2 * wave
    barsizefactor = bhealthmax / 10000
    healthbarblink = pygame.Rect(left + 35, top-5, int(100 * barsizefactor) + 10, 40)
    healthbarborder = pygame.Rect(left + 40, top, int(100 * barsizefactor), 30)
    healthbarfilled = pygame.Rect(left + 42, top + 2, int((196) * (health/(bhealthmax)) * barsizefactor), 26)

    if int((196) * (health/(bhealthmax))) > 70 * wave / 8:
        healthbarcolor = GREEN
    elif int((196) * (health/(bhealthmax))) > 30 * wave / 8:
        healthbarcolor = YELLOW
    else:
        healthbarcolor = RED

    if bosshealthblink < 10:
        pygame.draw.rect(screen, YELLOW, healthbarblink, 0, 2)
    else:
        pygame.draw.rect(screen, RED, healthbarblink, 0, 2)
    pygame.draw.rect(screen, BLACK, healthbarborder, 0, 2)
    pygame.draw.rect(screen, healthbarcolor, healthbarfilled, 0, 2)
    if bosshealthblink > 20:
        bosshealthblink = 0
    return boss
    

def armorbar(left, top, armor):
    armorbarborder = pygame.Rect(left + 240, top, armormax, 30)
    armorbarfilled = pygame.Rect(left + 242, top +2, int((armormax - 4) * (armor/(armormax/2))), 26)
    shieldimg = get_image("shield.png")
    shieldimg.set_colorkey(WHITE, RLEACCEL)
    armorbarmark = pygame.Rect(left + 337, top-3, 1, 33)
    pygame.draw.rect(screen, BLACK, armorbarborder, 0, 2)
    pygame.draw.rect(screen, BLUE, armorbarfilled, 0, 2)
    if armormax > 100:
        pygame.draw.rect(screen, BLACK, armorbarmark, 0, 0)
    #return healthmax
    screen.blit(shieldimg, (left + 212, top))
    return armor

def fpscounter():    
    fps = str(int(clock.get_fps()))
    fps_t = font20.render("FPS:" + fps, 1, RED)
    screen.blit(fps_t,(10,10))  

def statusdisplay():
    statusbox = pygame.Rect(3, SCREEN_HEIGHT - 97, SCREEN_WIDTH - 6, 94)
    statusboxframe = pygame.Rect(0,SCREEN_HEIGHT - 100,SCREEN_WIDTH,100)
    pygame.draw.rect(screen, BLUE, statusboxframe, 0, 3)
    pygame.draw.rect(screen, "#808080", statusbox, 0, 3)   
    cornimg = get_image("corner1a.png")
    cornimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(cornimg, (0, SCREEN_HEIGHT - 24))   
    cornimg = get_image("corner2.png")
    cornimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(cornimg, (0, SCREEN_HEIGHT - 100))
    cornimg = get_image("corner3a.png")
    cornimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(cornimg, (SCREEN_WIDTH - 24, SCREEN_HEIGHT - 100))
    cornimg = get_image("corner4.png")
    cornimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(cornimg, (SCREEN_WIDTH - 24, SCREEN_HEIGHT - 24))
    
    # Draw our game text
    texts(plives, score)
    texts2(flamer,shock,bio,pulse)   
    healthbar(120, SCREEN_HEIGHT - 85, player.hp)
    armorbar((healthmax + 170), SCREEN_HEIGHT - 85, player.armor)
    mgbar(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 85)
# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# make a controller
nojoy = False
try:
    controller = xbox360_controller.Controller()
except pygame.error:
    nojoy = True

# Create the screen object
# First set the icon
icon = pygame.image.load("graphics/icon.png")
icon.set_colorkey(WHITE, RLEACCEL)
pygame.display.set_icon(icon)
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
# Display = 0 picks the default monitor, and causes no error with only one monitor 
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT),display=0)
#screen = pygame.display.set_mode(size=(500, 500),display=1)
pygame.display.set_caption('Assault Shark')

# Preload graphics
def get_image(key):
    if not key in image_cache:
        image_cache[key] = pygame.image.load("graphics/" + key).convert()
    return image_cache[key]

image_cache = {}
# Gets a list of all images in the graphics directory
images = glob.glob ("Graphics/*.png")
# Loads all images into the image_cache dictionary
for image in images:
    img_name = os.path.basename(image)
    get_image(img_name)

# Preload JSON enemies
jsons = edict.addjsons()
print(str(jsons) + " JSON file(s) added")

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sounds/apoxode_-_electric_1.mp3")

# Load all our sound files
# Sound sources: Jon Fincher
# Many new additional sounds sourced from: http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
move_up_sound = pygame.mixer.Sound("sounds/rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds/falling_putter.ogg")
shoot_sound = pygame.mixer.Sound("sounds/shoot.ogg")
collision_sound = pygame.mixer.Sound("sounds/small_explosion.ogg")
bio_sound = pygame.mixer.Sound("sounds/bio_splat.ogg")
shock_sound = pygame.mixer.Sound("sounds/shock_sound2.ogg")
flamer_sound = pygame.mixer.Sound("sounds/flamer_sound.ogg")
powerup_sound = pygame.mixer.Sound("sounds/power_up.ogg")
wavechange_sound = pygame.mixer.Sound("sounds/wave_change.ogg")
pulse_sound = pygame.mixer.Sound("sounds/pulse_sound.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)
shoot_sound.set_volume(0.5)
bio_sound.set_volume(0.5)
shock_sound.set_volume(0.5)
flamer_sound.set_volume(0.5)
powerup_sound.set_volume(0.5)
wavechange_sound.set_volume(0.5)
pulse_sound.set_volume(0.5)

# Fill a nested dictionary of bullets by btype
bulletdict = {
    1: {
        "imgname": "bullet.png",
        "bspeed": 25,
        "sound": shoot_sound,
        "isanimated": False,
        "numframes": 1,
        "frames": ("bullet.png",),
        "frametimers": (0,)
    },
    2: {
        "imgname": "blast1.png",
        "shield": False,
        "bspeed": 20,
        "sound": flamer_sound,
        "isanimated": True,
        "numframes": 5,
        "frames": ("blast1.png","blast2.png","blast3.png","blast4.png","blast5.png"),
        "frametimers": (22,16,10,5,0)
    },
    3: {
        "imgname": "shock1.png",
        "shield": True,
        "bspeed": 0,
        "sound": shock_sound,
        "isanimated": True,
        "numframes": 4,
        "frames": ("shock1.png","shock2.png","shock3.png","shock4.png"),
        "frametimers": (12,8,4,0)
    },
    4: {
        "imgname": "bio1.png",
        "shield": False,
        "bspeed": 30,
        "sound": bio_sound,
        "isanimated": True,
        "numframes": 5,
        "frames": ("bio1.png","bio2.png","bio3.png","bio4.png","bio5.png"),
        "frametimers": (22,16,10,5,0)
    },
    5: {
        "imgname": "pulse1.png",
        "shield": False,
        "bspeed": 15,
        "sound": pulse_sound,
        "isanimated": True,
        "numframes": 5,
        "frames": ("pulse1.png","pulse2.png","pulse3.png","pulse4.png","pulse5.png"),
        "frametimers": (22,18,12,5,0)
    },
    6: {
        "imgname": "shockbolt.png",
        "shield": False,
        "bspeed": 0,
        "sound": shock_sound,
        "isanimated": True,
        "numframes": 2,
        "frames": ("shockbolt2.png", "shockbolt.png"),
        "frametimers": (2,0)
    }
}    



# Create sunmoon
wavesunmoon = SunMoon(0)
# Create our 'player'
player = Player(0)

# Create custom events for adding a new enemy and cloud and bullet and moving sun/moon
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDBULLET = pygame.USEREVENT + 3
pygame.time.set_timer(ADDBULLET, 50)
ADDMOUNTAIN = pygame.USEREVENT + 4
pygame.time.set_timer(ADDMOUNTAIN, 4000)
#MOVESUNMOON = pygame.USEREVENT + 4
#pygame.time.set_timer(MOVESUNMOON, 20000)

# Create groups to hold enemy sprites, cloud sprites, bullet sprites, mountain sprites, and all sprites
# - enemies, bullets, and mountains are used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
mountains = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# - wavesunmoon and player are individual sprites
all_sprites.add(wavesunmoon)
all_sprites.add(player)


# Now parameter lists for *params...

# parameters for the rboxipicwheels row for entering three initials video game style
# initialspos{} is the dictionary of options per wheel, with the ascii character literal and its rendering for
# all allowable ascii characters.  initialsdef{} is the default values of A, A, A.
# Initials defaults
initialfont = font50
initialfcolor = BLACK
# Dictionary for initial wheel positions
rendera = boxi.renderinits("A",initialfont, initialfcolor)
#rendera = rendera.subsurface(0,0,rendera.width - rendera.width//8, rendera.height)
#rendera = initialfont.render("A", 1, initialfcolor)
initialsdef = {1: {"lit": "A", "ren": rendera, "val": 65}, 2: {"lit": "A", "ren": rendera, "val": 65}, 3:{"lit": "A", "ren": rendera, "val": 65}}
# Programatically make an allowable ascii dictionary
initialspos = {}
ctr = 65 # Ascii value of "A" - capitals are 65 to 90, numbers are 48 to 57, but we want the numbers to appear after the letters
while ctr < 91:
    initialspos [ctr] = {"lit": chr(ctr), "ren": boxi.renderinits(chr(ctr), initialfont, initialfcolor)}
    ctr += 1
ctr = 48
while ctr < 58:
    initialspos [ctr] = {"lit": chr(ctr), "ren": boxi.renderinits(chr(ctr), initialfont, initialfcolor)}
    ctr += 1
# And the call defaults
initrboxidef = (screen, initialsdef, "ren", 830, 555, 2, YELLOW, 1, BLACK, initialspos, 0, 0)
# parameters for default boxi call with rendered text object - these will be extra field displays for the savegame Cboxiscroll
# A default rendered text item to display in a Boxi
textitem = font20.render("A text object", 1, BLACK)
# display boxes for loadgames
baseloc = (400, 1200)
boxidef1 = (screen, textitem, baseloc[0] + 30, baseloc[1], 0, LIGHTBLUE, 2, BLACK, 0, 0)
boxidef2 = (screen, textitem, baseloc[0] + 60, baseloc[1], 0, LIGHTBLUE, 2, BLACK, 0, 0)
boxidef3 = (screen, textitem, baseloc[0] + 90, baseloc[1], 0, LIGHTBLUE, 2, BLACK, 0, 0)
# parameters for a scrolling column of boxes, dictionary driven, with linked fields by key displayed
# Add a dictionary key "render" containing renders of the text keys
renderedtext = boxi.rendertextdic(edict.savedict, font20, RED)
cboxiscdef1 = (screen, renderedtext, "render", baseloc[0] + 160, baseloc[1] + 10, 1, WHITE, 1, BLUE, 0, 0, 7)

portalsetup = False
saved = False

# Set player lives, score, special weapons, redflash, greenflash, gamerunning variables

initials = "AAA"
# MG POWERUPS
# 1, 2, 3, 5, 7
mgmult = 1
# 1, 2, 3
mgtype = 1
# 0, 1, 2
mgbounce = 0
# x, y, speed, climb
bounceinheritc = 0
bounceinherits = 0
plives = 3
score = 0
flamer = 100
shock = 100
bio = 100
pulse = 100
player.hp = 100
player.armor = 50
healthmax = 200
armormax = 100
# For character deaths
redflash = False
# For stage changes
greenflash = False
# For flash timing
redflashticks = 0
greenflashticks = 0
# ingame being false steers to start screen - press enter to play
ingame = False
# pause state control
pause = False
# default if file not found
highscore = 0
# First wave setup
wave = 1
wavecounter = 0
wavegoal = 150
waveendticks = 0
# Tentacle attack not in progress
tentacleattack = False
jetupdown = 1
tilt = 1
lastwaveboss = 0
inportal = False
didicleanup = True
settingsscreen = False
settingssetup = False
# This call creates a .json file with all fields in the dictionary
# fullrec = edict.gencompleteblank()

# check for saved highscore
hsfilename = "highscore.txt"
if os.path.isfile(hsfilename) and os.access(hsfilename, os.R_OK):
    with open(hsfilename, "r") as file:
        hsstr =  file.read()
        if hsstr:
            hs = (int(hsstr))
        else:
            hs = 0
        # If larger than 0, update
        if hs > highscore:
            highscore = hs

didishowloadscreen = False
loadselection = False
loaddataexists = False
loaddataexists = edict.loadgame()
# returns number of saved games
listsize = edict.loadgame()
# Add rendered versions of savenames to dictionary
# Add a dictionary key "render" containing renders of the text keys
renderedtext = boxi.rendertextdic(edict.savedict, font20, RED)

playscreenupdated = False
pausescreenupdated = False
bosscheck = 0
addfactor = 0

def initnewgame():
    global loaded, loaddataexists
    global plives, score, flamer, shock, bio, pulse, redflash, greenflash, mgmult, mgtype, mgbounce, bounceinheritc, bounceinherits
    global healthmax, armormax,wave, wavecounter, wavegoal, waveboss, waveendticks, jetupdown, tilt, addfactor, bosscheck
    loaddataexists = False
    redflash = False
    greenflash = False
    bounceinheritc = 0
    bounceinherits = 0
    wavecounter = 0
    wavegoal = 150
    waveboss = 0
    waveendticks = 0
    jetupdown = 1
    tilt = 1
    pygame.mixer.music.play(loops=-1)
    wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
    wavesunmoon.update(wave)
    player.rect.left = 30
    player.rect.top = SCREEN_HEIGHT_NOBOX / 5
    if loaded:
        # Use loaded dictionary
        if loadgame != "":
            readgamedict(initsuff = loadgame)
        else:
            readgamedict()
    else:
        #Normal game start
        # MG POWERUPS
        # 1, 2, 3, 5, 7
        mgmult = 1
        # 1, 2, 3
        mgtype = 1
        # 0, 1, 2
        mgbounce = 0
        # x, y, speed, climb
        plives = 3
        score = 0
        flamer = 100
        shock = 100
        bio = 100
        pulse = 100
        wave = 1
        wavegoal = 150
        player.hp = 100
        player.armor = 50  
        healthmax = 200
        armormax = 100
        bosscheck = wave
        if (wave - 1) > 3: 
            addfactor += (wave - 1) // 3
            if addfactor > 3:
                addfactor = 3
        bosscheck += addfactor
        waveboss = bosscheck
    pygame.mixer.music.play(loops=-1)
    # New game has started, game loaded flag reset
    loaded = 0

# Variable to keep our main loop running - false is exit condition
running = True

# Our main loop
while running:
    try:
        #pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[K_m] and pressed_keys[K_LCTRL]:
            #move(Window)
            #pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT),display=0)
        if pause == True and ingame == True:
            # This is the 'paused' part of the game clock loop
            if inportal == True:
                # This is the 'in the vault' stub
                # 'In the vault' is a substate of paused
                if portalsetup == False:
                    screen.fill(BLACK)
                    mscreen = boxi.boxi(screen, get_image("sharktank3.png"), SCREEN_HEIGHT/2 - 512, SCREEN_WIDTH / 2 - 512, 3, GREEN, 3, YELLOW, 0, 0)
                    
                    instboxi = boxi.boxi(screen, vaulttext3red, SCREEN_HEIGHT - 30, SCREEN_WIDTH / 2 - vaulttext3red.width / 2, 2, BLACK, 3, RED, 0, 0)
                    if saved == False:
                        instboxi2 = boxi.boxi(screen, vaulttext5red, SCREEN_HEIGHT - 70, SCREEN_WIDTH / 2 - vaulttext5red.width / 2, 2, BLACK, 3, RED, 0, 0)
                    else:
                        instboxi2 = boxi.boxi(screen, vaulttext6red, SCREEN_HEIGHT - 70, SCREEN_WIDTH / 2 - vaulttext6red.width / 2, 2, BLACK, 3, RED, 0, 0)
                    screen.blit(vaulttext1red, (SCREEN_WIDTH / 2 - vaulttext1red.width/2, 810))
                    screen.blit(vaulttext2red, (SCREEN_WIDTH / 2 - vaulttext2red.width/2, 850))
                    screen.blit(vaulttext4red, (SCREEN_WIDTH / 2 - vaulttext4red.width/2, 890))
                    player.rect.bottom = 200
                    player.rect.left = 10
                    portalsetup = True
                    # Look at every event in the queue
                for event in pygame.event.get():
                    # Did the user hit a key?
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == xbox360_controller.START:
                            inportal = False
                            pause = False
                            pygame.mixer.music.play(loops=-1)
                        if event.button == xbox360_controller.BACK:
                            ingame = False                        
                        buttons = controller.get_buttons()
                        if buttons[0] == 1:
                            savegame()
                            saved = True 
                            portalsetup = False
                            stuff = False
                            # Save game
                            # Replace vaulttext5 with vaulttext6
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            # Press Enter to Play
                            # unpause
                            inportal = False
                            pause = False
                            pygame.mixer.music.play(loops=-1)
                        elif event.key == K_ESCAPE:
                            # Prepare for exit
                            ingame = False                                     
                        elif event.key == K_SPACE: 
                            savegame()
                            del instboxi2
                            saved = True
                            portalsetup = False
                            stuff = False     
                            # Save game
                            # Replace vaulttext5 with vaulttext6
                        #pressed_keysq = pygame.key.get_pressed()
                        #if pressed_keysq == K_p:
                        #    pause = False
                    # Did the user click the window close button? If so, stop the loop
                    elif event.type == QUIT:
                        running = False
                # Set Background for start screen     
                #screen.fill((135, 206, 250))
            else:
                if pausescreenupdated == False:
                    texts4()
                # Look at every event in the queue
                for event in pygame.event.get():
                    # Did the user hit a key?
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == xbox360_controller.START:
                            pause = False
                            pygame.mixer.music.play(loops=-1)
                        if event.button == xbox360_controller.BACK:
                            ingame = False
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            # Press Enter to Play
                            # unpause
                            inportal = False
                            pause = False
                            pygame.mixer.music.play(loops=-1)
                        elif event.key == K_ESCAPE:
                            # Prepare for exit
                            ingame = False              
                        #pressed_keysq = pygame.key.get_pressed()
                        #if pressed_keysq == K_p:
                        #    pause = False
                    # Did the user click the window close button? If so, stop the loop
                    elif event.type == QUIT:
                        running = False
                # Set Background for start screen     
                #screen.fill((135, 206, 250))
            
            pygame.display.flip()
        else:
            if ingame:
                # This is the primary play section of the main clock loop
                playscreenupdated = False
                pausescreenupdated = False
                didicleanup = False
                #pressed_keysq = pygame.key.get_pressed()
                #if pressed_keysq == K_p:
                #    pause = True
                # Look at events relative to pause status
                for event in pygame.event.get():
                # Did the user hit a key or button?
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == xbox360_controller.START:
                            pause = True
                            pygame.mixer.music.stop()                  
                    if event.type == KEYDOWN:
                        # Was it the Escape key? If so, stop the loop
                        if event.key == K_ESCAPE:
                            pause = True 
                        elif event.key == K_RETURN:
                            pause = True
                            pygame.mixer.music.stop()
                    # Did the user click the window close button? If so, stop the loop
                    elif event.type == QUIT:
                        running = False

                    # Should we add a new mountain?
                    elif event.type == ADDMOUNTAIN:
                        if redflash == False and greenflash == False:
                            # wave increases chance
                            if random.randint(1,100) < 25 + (2 * wave):
                                # Create the new mountain, and add it to our sprite groups
                                new_mountain = Mountain()
                                mountains.add(new_mountain)
                                all_sprites.add(new_mountain)


                    # Should we add a new enemy?
                    elif event.type == ADDENEMY:
                        if wavecounter < wavegoal:
                            # No new enemies while dead/wave 'Get Ready'
                            # Percentage of wave complete for factoring rate of enemy spawning
                            wavcompleteperc = int(((wavecounter + wave)/wavegoal) * 100)
                            # Possible to spawn boss at 50%
                            bosscheck = wave
                            if wave > 3: 
                                addfactor += (wave - 3) * 2
                            bosscheck += addfactor
                            
                            if wavcompleteperc > 50 and waveboss < bosscheck and bosses < 4 and random.randint(1,100) > 95:
                                new_enemy = Enemy("e_boss_cutboss41",35,edict.enemydict["e_boss_cutboss41"]["hp"],0)
                                enemies.add(new_enemy)
                                all_sprites.add(new_enemy)
                                new_enemy.hp = (new_enemy.hp / 2) * (wave / 2)
                                waveboss = waveboss + 1
                                lastwaveboss = wave
                            # if Boss hasn't spawned by 90%, spawn boss
                            if wavcompleteperc > 90 and lastwaveboss < wave:
                                new_enemy = Enemy("e_boss_cutboss41",35,edict.enemydict["e_boss_cutboss41"]["hp"],0)
                                enemies.add(new_enemy)
                                all_sprites.add(new_enemy)
                                new_enemy.hp = (new_enemy.hp / 2) * (wave / 2)
                                waveboss = waveboss + 1
                                lastwaveboss = wave

                            if random.randint(1,150) < wavcompleteperc + 25 + wave * wave:
                                enemiestocreate = random.randint(1,int(math.sqrt(wave)))
                                for x in range(1, enemiestocreate + 1):
                                    if redflash == False and greenflash == False:
                                        if 1==1:
                                            spawnlist = []
                                            spawnlist.clear()
                                            for pu in edict.enemydict: # See if enemy is allowable
                                                if edict.enemydict[pu]["firstspawn"] <= wave: # Wave allowed
                                                    # Don't release weapon upgrades player already has
                                                    dontadd = False
                                                    
                                                    if pu.startswith("e_pu_mgmult"): # Starts with powerup
                                                        if mgmult >= int(pu[-1]):
                                                            dontadd = True
                                                    if pu.startswith("e_pu_mgb"): # Starts with powerup
                                                        if mgbounce >= int(pu[-1]):
                                                            dontadd = True
                                                    if pu.startswith("e_pu_mgammo"): # Starts with powerup
                                                        if mgtype >= int(pu[-1]):
                                                            dontadd = True
                                                    if dontadd == False:
                                                        i = 1
                                                        while i <= edict.enemydict[pu]["spawnweight"]: # Likelyhood repeats of entries in list
                                                            spawnlist.append(pu)
                                                            i += 1
                                            choices = len(spawnlist)
                                            
                                            newetype = spawnlist[random.randint(1,choices) - 1]  # PIck one
                                            new_enemy = Enemy(newetype,15,edict.enemydict[newetype]["hp"],0)
                                            enemies.add(new_enemy)
                                            all_sprites.add(new_enemy)
                                        else:
                                            # Create the new enemy, and add it to our sprite groups
                                            hp = 1
                                            powerup = random.randint(1,100)
                                            if powerup < 3 + wave :
                                                # Blimp1
                                                newetype = "e_spawn_blimp4"
                                                hp = 10
                                            if powerup > 2 + wave and powerup < 5 + wave * 2:
                                                # Blimp2
                                                newetype = "e_spawn_blimpa5"
                                                hp = 20
                                            if powerup > 4 + wave * 2 and powerup < 7 + wave * 3:
                                                # Missile Launcher
                                                newetype = "e_g_misslaunch8"
                                            if powerup < 85 and powerup > 6 + wave * 3:
                                                # Missile
                                                newetype = "e_spawn_umiss1"
                                            elif powerup > 84 and powerup < 87:
                                                # Health
                                                newetype = "e_pu_health116"
                                                if healthmax < healthhardmax:
                                                    # 5 in 10 of boost to max health
                                                    if random.randint(1,10) > 5:
                                                        newetype = "e_pu_healthmax118"
                                            elif powerup > 86 and powerup < 89:
                                                # Armor
                                                newetype = "e_pu_armor117"
                                                if armormax < armorhardmax:
                                                    # 5 in 10 of boost to max armor
                                                    if random.randint(1,10) > 5:
                                                        newetype = "e_pu_armormax119"
                                            elif powerup > 88 and powerup < 93:
                                                # Extra Life
                                                newetype = "e_pu_life111"
                                                # Chance to spawn MG upgrades:
                                                if random.randint(1,10) > 3:
                                                    randslot = random.randint(1,3)
                                                    match randslot:
                                                        case 1:
                                                            # Ammo type upgrade
                                                            if wave > 2:
                                                                if mgtype < 3:
                                                                    newetype = "e_pu_mgammo_plasma"
                                                            elif wave > 1:
                                                                if mgtype < 2:
                                                                    newetype = "e_pu_mgammo_laser"
                                                        case 2:
                                                            # Bounce upgrade
                                                            if wave > 2:
                                                                if mgbounce < 3:
                                                                    newetype = "e_pu_mgb3"
                                                            elif wave > 1:
                                                                if mgbounce < 2:
                                                                    newetype = "e_pu_mgb2"
                                                            elif wave == 1:
                                                                if mgbounce < 0:
                                                                    newetype = "e_pu_mgb1"
                                                        case 3:
                                                            # Multishot upgrade
                                                            if wave > 3:
                                                                if mgmult < 7:
                                                                    newetype = "e_pu_mgmulti7"
                                                            elif wave > 2:
                                                                if mgmult < 5:
                                                                    newetype = "e_pu_mgmulti5"
                                                            elif wave > 1:
                                                                if mgmult < 3:
                                                                    newetype = "e_pu_mgmulti3"
                                                            elif wave == 1:
                                                                if mgmult < 2:
                                                                    newetype = "e_pu_mgmulti2"
                                                                

                                            elif powerup > 92 and powerup < 95:
                                                # Power Up FLamer
                                                newetype = "e_pu_flamer112"
                                            elif powerup > 94 and powerup < 97:
                                                # Power Up Shock
                                                newetype = "e_pu_shock113"
                                            elif powerup > 96 and powerup < 99:
                                                # Power Up Bio
                                                newetype = "e_pu_bio114"
                                            elif powerup > 97:
                                                # Power Up Pulse
                                                newetype = "e_pu_pulsar115"
                                            new_enemy = Enemy(newetype,14,hp,0)
                                            enemies.add(new_enemy)
                                            all_sprites.add(new_enemy)
                                        oops = pygame.sprite.spritecollideany(new_enemy, mountains)
                                        if oops:
                                            if new_enemy.etype.startswith("e_g") == False:
                                                new_enemy.kill()

                    # Should we add a new cloud?
                    elif event.type == ADDCLOUD:
                        # Create the new cloud, and add it to our sprite groups
                        new_cloud = Cloud()
                        clouds.add(new_cloud)
                        all_sprites.add(new_cloud)

                    # Should we add a new bullet?
                    elif event.type == ADDBULLET:
                        if player.firebullet > 0 and player.firebullet < 4:
                            # Create the new bullet, and add it to our sprite groups
                            match mgmult:
                                case 1:
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                case 2:
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 9,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom - 9,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                case 3:
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 18,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom - 18,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                case 5:
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 36,1,9)
                                    bullets.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 18,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom - 18,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + -36,1,10)
                                    bullets.add(new_bullet)
                                case 7:
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 54,1,11)
                                    bullets.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 36,1,9)
                                    bullets.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + 18,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom - 18,1,8)
                                    bullets.add(new_bullet)
                                    all_sprites.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + -36,1,10)
                                    bullets.add(new_bullet)
                                    new_bullet = Bullet(player.rect.right,player.rect.bottom + -54,1,12)
                                    bullets.add(new_bullet)
                            
                            player.firebullet = player.firebullet - 1 
                        elif player.firebullet == 4:
                            # Create the blast bullet, and add it to our sprite groups
                            # Decrement armory
                            if flamer > 0:
                                flamer = flamer - 1
                                new_bullet = Bullet(player.rect.right,player.rect.top,2,30)
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)    
                            player.firebullet = 0
                            
                        elif player.firebullet == 5:
                            # Create the lightning shield, and add it to our sprite groups
                            # Decrement armory
                            if shock > 0:
                                shock = shock - 1
                                new_bullet = Bullet(player.rect.right - player.rect.width/2, player.rect.top + player.rect.height/2,3,16)      
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)
                            player.firebullet = 0
                        elif player.firebullet == 6:
                            # Create the bioweapon bullet, and add it to our sprite groups
                            # Decrement armory
                            if bio > 0:
                                bio = bio - 1
                                new_bullet = Bullet(player.rect.right,player.rect.top,4,26)
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)
                            player.firebullet = 0
                        elif player.firebullet == 7:
                            # Create the pulse bullet and add it to our sprite groups
                            # Decrement armory
                            if pulse > 0:
                                pulse = pulse - 1
                                new_bullet = Bullet(player.rect.right, player.rect.top,5,65)
                                bullets.add(new_bullet)
                                all_sprites.add(new_bullet)
                            player.firebullet = 0                    
                # Get the set of keys pressed and check for user input
                if redflash or greenflash:
                    # Keep player off screen for flash
                    player.rect.right = -300
                else:
                    #unhide player
                    pressed_keys = pygame.key.get_pressed()
                    player.update(pressed_keys)
                    #player.rect.left = 30

                pressed_keys = pygame.key.get_pressed()
                player.update(pressed_keys)

                # Fill the screen with wave-appropriate sky blue unless redflash or greenflash
                if redflash:
                    screen.fill((RED))
                    if pygame.time.get_ticks() > redflashticks + 3000:
                        redflash = False
                        player.rect.left = 30
                        pygame.mixer.music.play(loops=-1)
                elif greenflash:
                    screen.fill(GREEN)
                    if pygame.time.get_ticks() > greenflashticks + 3000:
                        greenflash = False
                        player.rect.left = 30
                        pygame.mixer.music.play(loops=-1)
                else:
                    if wave < 4:
                        screen.fill((135 / wave, 206 / wave, 250 / wave))
                        # Evening sky
                    elif wave > 3 and wave < 5:
                        screen.fill((0, 0, 25))
                        # Dark sky
                    elif wave > 4:
                        screen.fill((0,0,5))
                        # Late Night Sky

                # Update the position of our enemies, bullets, and clouds
                wavesunmoon.update(wave)
                mountains.update()
                bullets.update()
                enemies.update()
                
                #player.update(pressed_keys)
                clouds.update()
                
                # Draw all our sprites
                #while True:
                
                screen.blit(wavesunmoon.surf, wavesunmoon.rect)
                screen.blit(player.surf, player.rect)
                for entity in mountains:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                for entity in bullets:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                for entity in enemies:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                for entity in clouds:
                    if hasattr(entity, "rect") and hasattr(entity, "surf"):
                        screen.blit(entity.surf, entity.rect)
                
                #for entity in all_sprites:
                #    screen.blit(entity.surf, entity.rect)
                # Draw our status box, add texts
                bosses = 0
                bossmode = False
                for e in enemies:
                    if edict.enemydict[e.etype]["boss"] == 1:
                        bossmode = True
                        bosses += 1
                        bhealthmax = edict.enemydict[e.etype]["hp"] / 4 * wave
                        barsizefactor = bhealthmax / 1000
                        barwide = 200 * barsizefactor + 10
                        bosshealthbar((SCREEN_WIDTH / 2 - (barwide // 2)), (bosses * 50), e ,e.hp, bosshealthblink)
                        bosshealthblink = bosshealthblink + 1
                        if bosshealthblink > 20:
                            bosshealthblink = 0
                # Spawn shower of powerups - the boss is dead
                # Score being non zero blocks bonus spawn at game beginning after lost bossfight            
                if bossmode == False and wasbossmode == True and score > 0:
                    pups = wave * 10 # E to spawn
                    newe = 0 # E being spawned
                    spawnlist = []
                    for pu in edict.enemydict: # See if enemy is allowable
                        if pu.startswith("e_pu"): # Starts with powerup
                            if edict.enemydict[pu]["firstspawn"] <= wave: # Wave allowed
                                i = 1
                                while i <= edict.enemydict[pu]["spawnweight"]: # Likelyhood repeats of entries in list
                                    dontadd = False
                                                    
                                    if pu.startswith("e_pu_mgmult"): # Starts with powerup
                                        if mgmult >= int(pu[-1]):
                                            dontadd = True
                                    if pu.startswith("e_pu_mgb"): # Starts with powerup
                                        if mgbounce >= int(pu[-1]):
                                            dontadd = True
                                    if pu.startswith("e_pu_mgammo"): # Starts with powerup
                                        if mgtype >= int(pu[-1]):
                                            dontadd = True
                                    if dontadd == False:
                                        spawnlist.append(pu)
                                    i += 1
                    choices = len(spawnlist)
                    while newe < pups:
                        newtype = spawnlist[random.randint(1,choices) - 1]  # PIck one
                        hp = 1
                        new_enemy = Enemy(newtype,35,hp,0)
                        enemies.add(new_enemy)
                        all_sprites.add(new_enemy)
                        newe += 1
                wasbossmode = bossmode
                statusdisplay()

                if redflash:
                    pygame.mixer.music.stop()
                    #Count down on get ready message - has to occur after sprites
                    counterstr = ""
                    #font = pygame.font.Font("fonts/arcade_r.ttf",30)
                    deadtext = font30.render("You Died!  Lives remain: " + str(plives), 1, BLACK)
                    dtxtoffset = deadtext.width / 2
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset, 200))
                    deadtext = font30.render("You Died!  Lives remain: " + str(plives), 1, BLUE)
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset + 2, 202))
                    # Bigger font for the countdown
                    #font = pygame.font.Font("fonts/arcade_r.ttf",75) 
                    if pygame.time.get_ticks() > redflashticks + 2500:
                        counterstr = "1"
                    elif pygame.time.get_ticks() > redflashticks + 2000:
                        counterstr = "2"
                    elif pygame.time.get_ticks() > redflashticks + 1500:
                        counterstr = "3"
                    elif pygame.time.get_ticks() > redflashticks + 1000:
                        counterstr = "4"
                    elif pygame.time.get_ticks() > redflashticks + 500:
                        counterstr = "5"           
                    countertext = font75.render("GET READY: " + counterstr, 1, BLACK)
                    ctxtoffset = countertext.width / 2
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset, SCREEN_HEIGHT / 2))          
                    countertext = font75.render("GET READY: " + counterstr, 1, BLUE)
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset + 2, SCREEN_HEIGHT / 2 + 2))  
                elif greenflash:
                    #Count down on get ready message - has to occur after sprites
                    pygame.mixer.music.stop()
                    counterstr = ""
                    #font = pygame.font.Font("fonts/arcade_r.ttf",30)
                    deadtext = font30.render("Wave #" + str(wave) + " (0/" +str(wavegoal) + ")", 1, BLACK)
                    dtxtoffset = deadtext.width / 2
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset, 200))
                    deadtext = font30.render("Wave #" + str(wave) + " (0/" +str(wavegoal) + ")", 1, BLUE)
                    screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset + 2, 202))
                    # Bigger font for the countdown
                    #font = pygame.font.Font("fonts/arcade_r.ttf",75) 
                    if pygame.time.get_ticks() > greenflashticks + 2500:
                        counterstr = "1"
                    elif pygame.time.get_ticks() > greenflashticks + 2000:
                        counterstr = "2"
                    elif pygame.time.get_ticks() > greenflashticks + 1500:
                        counterstr = "3"
                    elif pygame.time.get_ticks() > greenflashticks + 1000:
                        counterstr = "4"
                    elif pygame.time.get_ticks() > greenflashticks + 500:
                        counterstr = "5"           
                    countertext = font75.render("GET READY: " + counterstr, 1, BLACK)
                    ctxtoffset = countertext.width / 2
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset, SCREEN_HEIGHT / 2))          
                    countertext = font75.render("GET READY: " + counterstr, 1, BLUE)
                    screen.blit(countertext, (SCREEN_WIDTH / 2 - ctxtoffset + 2, SCREEN_HEIGHT / 2 + 2))

                # Check if the player has collided with any mountains
                crash = pygame.sprite.spritecollideany(player, mountains)
                if crash:
                    crash.mask = pygame.mask.from_surface(crash.surf)
                    if pygame.sprite.collide_mask(player, crash):
                        # If portal!
                        if crash.name.startswith("portal") and player.rect.left < crash.rect.left and player.rect.top > crash.rect.top + 25:
                            #player has gone through portal
                            portalmountain = crash
                            inportal = True
                            portalsetup = False
                            pause = True
                            saved = False
                        else:
                            # Decrement lives
                            plives = plives - 1
                            redflash = True
                            redflashticks = pygame.time.get_ticks()
                            # Move player position to hide
                            player.rect.left = -300
                            player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                            # Refill health
                            player.hp = 100
                            # Refill armor
                            player.armor = 50
                            # Cause destruction event for any remaining enemies
                            for i, enemy1 in enumerate(enemies):
                                if enemy1.etype != "e_boss_cutboss41":
                                    enemy1.boomcounter = 10
                                    if edict.enemydict[enemy1.etype]["isexplodable"]:
                                        enemy1.etype = edict.enemydict[enemy1.etype]["isexplodable"]
                                    else:
                                        if edict.enemydict[enemy1.etype]["boss"] == False:
                                            enemy1.kill()
                                    score = score + 1
                                    wavecounter = wavecounter + 1                                                           
                            # If no lives remain, kill player
                            if plives < 1:
                                for i, enemy1 in enumerate(enemies):
                                    enemy1.kill()
                                # Go to start screen
                                ingame = False

                # Check if any enemies have collided with the player
                # PLAYER ENEMY COLLISIONS
                
                # Make sure all enemies have rectangles
                #for e in enemies:
                    #if e.etype == 91:
                    #if hasattr(e, "rect") == False:
                    #    e.kill()
                crash = pygame.sprite.spritecollideany(player, enemies)
                if crash:
                    crash.mask = pygame.mask.from_surface(crash.surf)
                    if pygame.sprite.collide_mask(player, crash):
                        #if crash.etype == 91:
                        if edict.enemydict[crash.etype]["ispowerup"] == False:
                            # Missile or blimp, possibly exploding
                            collision_sound.play()
                            # Implement variable damage
                            damage = random.randint(*edict.enemydict[crash.etype]["damage"])
                            # if player has armor left
                            if player.armor > 0:
                                # Damage armor first
                                player.armor = player.armor - damage
                                # If armor exhausted
                                if player.armor < 0:
                                    # Remove remainder from health
                                    player.hp = + player.hp + player.armor
                                    # Set armor to empty
                                    player.armor = 0
                            else:
                                player.hp = player.hp - damage
                            if player.hp < 1:
                                # Decrement lives
                                plives = plives - 1
                                redflash = True
                                redflashticks = pygame.time.get_ticks()
                                # Move player position to hide
                                player.rect.left = -300
                                player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                                # Refill health
                                player.hp = 100
                                # Refill armor
                                player.armor = 50
                                # Cause destruction event for any remaining enemies
                                for i, enemy1 in enumerate(enemies):
                                    if enemy1.etype != "e_boss_cutboss41":
                                        enemy1.boomcounter = 10
                                        if edict.enemydict[enemy1.etype]["isexplodable"]:
                                            enemy1.etype = edict.enemydict[enemy1.etype]["isexplodable"]
                                        else:
                                            enemy1.kill()
                                        score = score + 1
                                        wavecounter = wavecounter + 1                                                           
                            # If no lives remain, kill player
                            if plives < 1:
                                for i, enemy1 in enumerate(enemies):
                                    enemy1.kill()
                                # Go to start screen
                                ingame = False
                        
                        elif crash.etype == "e_pu_life111":
                            # Extra Life
                            plives = plives + 1
                        elif crash.etype == "e_pu_flamer112":
                            # Power Up Flamer
                            flamer = flamer + 100
                        elif crash.etype == "e_pu_shock113":
                            # Power Up Shock
                            shock = shock + 100
                        elif crash.etype == "e_pu_bio114":
                            # Power Up Bio
                            bio = bio + 100
                        elif crash.etype == "e_pu_pulsar115":
                            # Power Up Pulsar
                            pulse = pulse + 100
                        elif crash.etype == "e_pu_health116":
                            # Power Up Health
                            newnumber(edict.blue16nums[50],(player.rect.left, player.rect.top))
                            player.hp = player.hp + 50
                            if player.hp > healthmax // 2:
                                player.hp = healthmax // 2 
                        elif crash.etype == "e_pu_armor117":
                            # Power Up Armor
                            player.armor = player.armor + 25
                            if player.armor > armormax // 2:
                                player.armor = armormax // 2
                        elif crash.etype == "e_pu_healthmax118":
                            newnumber(edict.blue16nums[50],(player.rect.left, player.rect.top))
                            # Raise maximum health
                            healthmax = healthmax + 50
                            if healthmax > healthhardmax:
                                healthmax = healthhardmax
                            # Power Up Health
                            player.hp = player.hp + 50
                            if player.hp > healthmax // 2:
                                player.hp = healthmax // 2  
                        elif crash.etype == "e_pu_armormax119":
                            # Raise maximum armor
                            armormax = armormax + 25
                            if armormax > armorhardmax:
                                armormax = armorhardmax
                            # Power Up Armor
                            player.armor = player.armor + 25
                            if player.armor > armormax // 2:
                                player.armor = armormax // 2
                        elif crash.etype == "e_pu_mgmulti2":
                            # MG upgrade multifire 2
                            mgmult = 2
                        elif crash.etype == "e_pu_mgmulti3":
                            # MG upgrade multifire 3
                            mgmult = 3
                        elif crash.etype == "e_pu_mgmulti5":
                            # MG upgrade multifire 5
                            mgmult = 5
                        elif crash.etype == "e_pu_mgmulti7":
                            # MG upgrade multifire 7
                            mgmult = 7
                        elif crash.etype == "e_pu_mgammo_laser2":
                            # MG upgrade laser ammo
                            mgtype = 2
                        elif crash.etype == "e_pu_mgammo_plasma3":
                            # MG upgrade plasma ammo
                            mgtype = 3
                        elif crash.etype == "e_pu_mgb1":
                            # MG upgrade bounce ammo
                            mgbounce = 1
                        elif crash.etype == "e_pu_mgb2":
                            # MG upgrade 2 bounce ammo
                            mgbounce = 2
                        elif crash.etype == "e_pu_mgb3":
                            # MG upgrade 3 bounce ammo
                            mgbounce = 3                            
                        


                        # Remove the Enemy if not boss or tentacle
                        if edict.enemydict[crash.etype]["boss"] == 0 and crash.etype != 91:
                            #if crash.etype == 91:
                            crash.kill()
                        else:
                            # Player bounces off boss
                            if player.rect.centerx < crash.rect.centerx:
                                player.rect.right = crash.rect.left - 50
                                player.speed = crash.speed + 3
                            else:
                                player.rect.left = crash.rect.right + 50
                                player.speed = crash.speed - 3
                            if player.rect.centery < crash.rect.centery:
                                player.rect.bottom = crash.rect.top - 50
                                player.climb = crash.climb - 3
                            else:
                                player.rect.top = crash.rect.bottom + 50
                                player.climb = crash.climb + 3
                        # Stop any moving sounds and play the collision sound
                        move_up_sound.stop()
                        move_down_sound.stop()
                        shoot_sound.stop()
                        bio_sound.stop()
                        shock_sound.stop()
                        flamer_sound.stop()
                        powerup_sound.stop()
                        wavechange_sound.stop()
                        pulse_sound.stop()
                        if edict.enemydict[crash.etype]["ispowerup"] == False:
                            # If hostile
                            collision_sound.play()
                        elif edict.enemydict[crash.etype]["ispowerup"]:
                            # If powerup
                            score = score + 25
                            wavecounter = wavecounter + 1
                            powerup_sound.play()
                # Check for other collisions, kill colliding enemies and destructable bullets   
                # ENEMY ENEMY COLLISIONS
                # Make sure all enemies have rectangles
                #for e in enemies:
                #    if hasattr(e, "rect") == False:
                #        e.kill()
                for i, enemy1 in enumerate(enemies):
                    enemy2 = pygame.sprite.spritecollideany(enemy1, enemies)
                    # If enemies collide
                    if enemy2 != enemy1: 
                        #if enemy2.etype == 91:
                        #if enemy1.etype == 91:
                        # Not with themselves
                        # De-collide, move smaller
                        #enemy2.rect = enemy2.surf.get_rect()
                        # If enemy2 is smaller and not tentacle or boss
                        if ((enemy2.rect.height * enemy2.rect.width) < (enemy1.rect.height * enemy1.rect.width)) and enemy2.etype != "e_tent_tentacle91" and enemy2.etype != "e_boss_cutboss41":
                            if enemy2.rect.centerx < enemy1.rect.centerx:
                                enemy2.rect.right = enemy1.rect.left -5
                            else:
                                enemy2.rect.left = enemy1.rect.right +5
                        elif enemy1.etype != "e_tent_tentacle91" and enemy1.etype != "e_boss_cutboss41":
                            if enemy1.rect.centerx < enemy2.rect.centerx:
                                enemy1.rect.right = enemy2.rect.left -5
                            else:
                                enemy1.rect.left = enemy2.rect.right +5
                        
                        # 2 powerups don't hurt eachother
                        if not(edict.enemydict[enemy1.etype]["ispowerup"] and edict.enemydict[enemy2.etype]["ispowerup"]):
                            collision_sound.play()
                            if edict.enemydict[enemy1.etype]["isexploded"] == False:
                                # is enemy immune?
                                if edict.enemydict[enemy1.etype]["damenemies"] > 0:
                                    dam = random.randint(5,15)
                                    enemy1.hp = enemy1.hp - dam
                                    newnumber(edict.yellow16nums[dam],(thisenemy.rect.left, thisenemy.rect.top))
                                    if enemy1.hp < 1:
                                        if edict.enemydict[enemy1.etype]["isexplodable"]:
                                            enemy1.etype = edict.enemydict[enemy1.etype]["isexplodable"]
                                        else:
                                            enemy1.kill()
                                        score = score + edict.enemydict[enemy1.etype]["hp"]
                                        wavecounter = wavecounter + 1
                            if edict.enemydict[enemy2.etype]["isexploded"] == False:                           
                                # is enemy immune?
                                if edict.enemydict[enemy2.etype]["damenemies"] > 0:
                                    dam = random.randint(5,15)
                                    enemy2.hp = enemy2.hp - dam
                                    newnumber(edict.yellow16nums[dam],(thisenemy.rect.left, thisenemy.rect.top))
                                    if enemy2.hp < 1:
                                        if edict.enemydict[enemy2.etype]["isexplodable"]:
                                            enemy2.etype = edict.enemydict[enemy2.etype]["isexplodable"]
                                        else:
                                            enemy2.kill()
                                        score = score + edict.enemydict[enemy2.etype]["hp"]
                                        wavecounter = wavecounter + 1
                # BULLET ENEMY COLLISIONS  
                # Make sure all enemies have rectangles
                for e in enemies:
                    if hasattr(e, "rect") == False:
                        e.kill()      
                for i, thisenemy in enumerate(enemies):
                    bullethit = pygame.sprite.spritecollideany(thisenemy, bullets)
                    # If bullet hits enemy
                    if bullethit:
                        #newnumber(edict.red16nums[edam],(thisenemy.rect.left, thisenemy.rect.top))
                        collision_sound.play()
                        if edict.enemydict[thisenemy.etype]["isexploded"] == False and edict.enemydict[thisenemy.etype]["ispowerup"] == False:
                            edam = random.randint(5,15)
                            if bullethit.btype == 1 and mgtype > 1:
                                if mgtype == 2:
                                    edam = random.randint(15,25)
                                if mgtype == 3:
                                    edam = random.randint(23,38)
                            
                            newnumber(edict.red16nums[edam],(thisenemy.rect.left, thisenemy.rect.top))
                            thisenemy.hp -= edam
                            if thisenemy.hp < 1:
                                if edict.enemydict[thisenemy.etype]["isexplodable"]:
                                    thisenemy.etype = edict.enemydict[thisenemy.etype]["isexplodable"]
                                else:
                                    thisenemy.kill()
                                score = score + edict.enemydict[thisenemy.etype]["hp"]
                                wavecounter += 1
                                
                                newnumber(edict.green16nums[edict.enemydict[thisenemy.etype]["hp"]],(thisenemy.rect.left, thisenemy.rect.top))
                            if bullethit.btype == 1:
                                # MG bullets go away on impact
                                breakage = random.randint(1,10)
                                if mgtype == 1:
                                    if breakage > 1:
                                        bullethit.kill()
                                        newnumber(edict.yellow16nums[breakage],(thisenemy.rect.left, thisenemy.rect.top))
                                if mgtype == 2:
                                    # Laser bullets 50% destroyed
                                    if breakage > 5:
                                        bullethit.kill()
                                        newnumber(edict.yellow16nums[breakage],(thisenemy.rect.left, thisenemy.rect.top))
                                if mgtype == 3:
                                    # Plasma bullets 20% destroyed
                                    if breakage > 8:
                                        bullethit.kill()
                                        newnumber(edict.yellow16nums[breakage],(thisenemy.rect.left, thisenemy.rect.top))
                           
                            else:
                                # Large bullets degraded by impacts
                                bullethit.boomcounter -= 1                                       
                                newnumber(edict.yellow16nums[1],(thisenemy.rect.left, thisenemy.rect.top))                    
                # BULLET MOUNTAIN COLLISIONS        
                for i, thismountain in enumerate(mountains):
                    bullethit = pygame.sprite.spritecollideany(thismountain, bullets)
                    if bullethit:
                        if bullethit.btype == 1:
                            bullethit.kill()
                        else:
                            # Large bullets seriously degraded by mountains
                            if bullethit.boomcounter > 2:
                                bullethit.boomcounter = 2
                # ENEMY MOUNTAIN COLLISIONS  
                # Make sure all enemies have rectangles
                for e in enemies:
                    if hasattr(e, "rect") == False:
                        e.kill()         
                for i, thismountain in enumerate(mountains):
                    enemyhit = pygame.sprite.spritecollideany(thismountain, enemies)
                    if enemyhit:
                        if enemyhit.etype.startswith("e_g") == False: #cannon sit on mountain, missile launchers stay on ground
                            # Move enemy up
                            enemyhit.rect.bottom -= 50
                            enemyhit.climb = -3
                            # Bounce enemy left/right from mountain
                            if enemyhit.rect.centerx < thismountain.rect.centerx:
                                enemyhit.rect.right = thismountain.rect.left - 10
                                enemyhit.speed = 4
                            else:
                                enemyhit.rect.left = thismountain.rect.right + 10
                                enemyhit.speed = 6
                        if edict.enemydict[enemyhit.etype]["isexploded"] == False:
                            if enemyhit.etype.startswith("e_g") == False : #cannon sit on mountain  #STARTSWITH this
                                # If enemy takes damage from mountain collisions 
                                if edict.enemydict[enemyhit.etype]["dammountain"] > 0:      
                                    # Calculate partial immunity if applicable                 
                                    enemyhit.hp = enemyhit.hp - int(100 * edict.enemydict[enemyhit.etype]["dammountain"] / 100)
                                    if enemyhit.hp < 0:
                                        if edict.enemydict[enemyhit.etype]["isexplodable"]:
                                            enemyhit.etype = edict.enemydict[enemyhit.etype]["isexplodable"]
                                        else:
                                            if edict.enemydict[enemyhit.etype]["isexploded"] == False:
                                                enemyhit.kill()
                                        score = score + 1
                if wavecounter > wavegoal or wavecounter == wavegoal:
                    if bossmode == False:
                        waveendticks += 1
                    if len(enemies) == 0 or waveendticks > 250:
                        # Set up next wave
                        jetupdown = 1
                        tilt = 1
                        wave = wave + 1
                        wavegoal = wavegoal + (wave * wave * 10) + 100
                        wavecounter = 0
                        waveendticks = 0
                        jetupdown = 1
                        tilt = 1
                        # Green flash for wave complete
                        greenflash = True
                        greenflashticks = pygame.time.get_ticks()
                        move_up_sound.stop()
                        move_down_sound.stop()
                        shoot_sound.stop()
                        collision_sound.stop()
                        bio_sound.stop()
                        shock_sound.stop()
                        flamer_sound.stop()
                        powerup_sound.stop()
                        pulse_sound.stop()
                        wavechange_sound.play()
                        # Move player positon to hide
                        player.rect.left = -300
                        player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                        # update sunmoon state & new random position
                        wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
                        wavesunmoon.update(wave)
                if score > highscore:
                    highscore = score
                # Flip everything to the display
                pygame.display.flip()
                
                # Ensure we maintain a 30 frames per second rate
                clock.tick(30)
            else:
                if settingsscreen == True:
                    # This is the settings / initials screen showing part of the clock loop
                    if settingssetup == False:
                        screen.fill(BLACK)
                        sscreen = boxi.boxi(screen, get_image("settingsscreen.png"), SCREEN_HEIGHT/2 - 512, SCREEN_WIDTH / 2 - 512, 3, GREEN, 3, YELLOW, 0, 0)                  
                        # rboxi for initials
                        initialsrboxi = boxi.rboxipicwheels(*initrboxidef, tabord = 2)
                        # And we register the new control
                        #initialsrboxi.register()
                        # Boxibutton for randomizing initials - this passes a function hook for the button pressed event
                        randomizeinitsboxibutton = boxi.boxibutton(480, 900, 100, 30, 3, YELLOW, 1, BLACK, randomizebutton, 5, "Randomize Initials", screen)
                        # And we register the new control
                        #randomizeinitsboxibutton.register()
                        randomizeinitsboxibutton.frame.bordercolor = boxi.gotfocuscolor
                        instboxi = boxi.boxi(screen, settextred, SCREEN_HEIGHT - 30, SCREEN_WIDTH / 2 - settextred.width / 2, 2, BLACK, 3, RED, 0, 0)
                        instboxi2 = boxi.boxi(screen, settextred2, SCREEN_HEIGHT - 65, SCREEN_WIDTH / 2 - settextred2.width / 2, 2, BLACK, 3, RED, 0, 0)                               
                        jtimeout = 0
                        settingssetup = True
                    # Look at every event in the queue
                    if randomizeinitsboxibutton != None and initialsrboxi != None:
                        for event in pygame.event.get():
                            # Did the user hit a key or joystick button?
                            if nojoy != True:
                                if event.type == pygame.JOYBUTTONDOWN:
                                    if event.button == xbox360_controller.START:
                                        stuff = False                         
                                    if event.button == xbox360_controller.BACK:
                                        # Return to main screen
                                        didicleanup = False
                                        settingsscreen = False
                                        #running = False   
                                left_x, left_y = controller.get_left_stick()
                                if left_y > .2:
                                    if jtimeout < 1:
                                        initialsrboxi.updatebuttons(K_DOWN)
                                        jtimeout = 7
                                    if jtimeout > 0:
                                        jtimeout -=1        
                                elif left_y < -.2:
                                    if jtimeout < 1:
                                        initialsrboxi.updatebuttons(K_UP)
                                        jtimeout = 7
                                    if jtimeout > 0:
                                        jtimeout -=1  
                                elif left_x > .2:
                                    if jtimeout < 1:
                                        initialsrboxi.updatebuttons(K_RIGHT)
                                        jtimeout = 7
                                    if jtimeout > 0:
                                        jtimeout -=1    
                                elif left_x < -.2:
                                    if jtimeout < 1:
                                        initialsrboxi.updatebuttons(K_LEFT)
                                        jtimeout = 7
                                    if jtimeout > 0:
                                        jtimeout -=1                               
                                triggers = controller.get_triggers()
                                buttons = controller.get_buttons()
                                if triggers > 0.3:
                                    stuff = False
                                if buttons[0] == 1:
                                    #if jtimeout < 1:
                                    initials = initialsrboxi.textstr
                                    didicleanup = False
                                    settingsscreen = False 
                                    #jtimeout = 10
                                if buttons[2] == 1:
                                    stuff = False
                                if buttons[1] == 1:
                                    stuff = False
                                if buttons[3] == 1:
                                    randomizeinitsboxibutton.buttonpressed(randomizeinitsboxibutton.getbuttonpressed)
                                    randomizeinitsboxibutton.rectborder.top = randomizeinitsboxibutton.rectbox.top - randomizeinitsboxibutton.border2
                                    randomizeinitsboxibutton.rectborder.left = randomizeinitsboxibutton.rectbox.left - randomizeinitsboxibutton.border2
                                    randomizeinitsboxibutton.pressedshadow = True
                                    rbuttimer = 5
                                if buttons[4] == 1:        
                                    stuff = False    
                            if event.type == KEYDOWN:
                                if event.key == K_RETURN:
                                    initials = initialsrboxi.textstr
                                    didicleanup = False
                                    settingsscreen = False
                                elif event.key == K_ESCAPE:
                                    # Return to main screen
                                    didicleanup = False
                                    settingsscreen = False
                                elif event.key == K_DOWN or event.key == K_UP or event.key == K_LEFT or event.key == K_RIGHT:
                                    initialsrboxi.updatebuttons(event.key)  
                                elif event.key == K_SPACE:
                                    randomizeinitsboxibutton.buttonpressed(randomizeinitsboxibutton.getbuttonpressed)
                                    randomizeinitsboxibutton.rectborder.top = randomizeinitsboxibutton.rectbox.top - randomizeinitsboxibutton.border2
                                    randomizeinitsboxibutton.rectborder.left = randomizeinitsboxibutton.rectbox.left - randomizeinitsboxibutton.border2
                                    randomizeinitsboxibutton.pressedshadow = True
                                    rbuttimer = 5
                            if event.type == MOUSEBUTTONDOWN:
                                mousepos = pygame.mouse.get_pos()
                                boxi.mousehandler(event, event.button, mousepos)
                            if event.type == MOUSEWHEEL:
                                boxi.mousehandler(event, 0, (0, event.y)) 
                            if event.type == MOUSEBUTTONUP:
                                randomizeinitsboxibutton.rectborder.top = randomizeinitsboxibutton.rectbox.top 
                                randomizeinitsboxibutton.rectborder.left = randomizeinitsboxibutton.rectbox.left 
                    
                        if jtimeout > 0:
                            jtimeout -=1    
                    if settingsscreen == True:
                        if rbuttimer > 0:
                            rbuttimer -= 1
                            if rbuttimer == 0:
                                if randomizeinitsboxibutton:
                                    randomizeinitsboxibutton.rectborder.top = randomizeinitsboxibutton.rectbox.top 
                                    randomizeinitsboxibutton.rectborder.left = randomizeinitsboxibutton.rectbox.left

                        # This is an animation handler for the initials rboxi's randomize initials function, called by the rboxi button above.
                        # It serves no vital purpose, but displays the scrolling of the initials as if it were a slot machine, which is fun.    
                        if a1 > 0 or a2 > 0 or a3 > 0:
                            isanioverflag = False
                            isaniover = 3
                            if a1 > 0:
                                a1 -= 1
                                if initialsrboxi:
                                    initialsrboxi.selectedcol = 0
                                    initialsrboxi.turnwheeldown()
                                    initialsrboxi.rdict[initialsrboxi.selectedcol]["boxi"].draw()
                            if a2 > 0:
                                a2 -= 1
                                if initialsrboxi:
                                    initialsrboxi.selectedcol = 1
                                    initialsrboxi.turnwheeldown()
                                    initialsrboxi.rdict[initialsrboxi.selectedcol]["boxi"].draw()
                            if a3 > 0:
                                a3 -= 1
                                if initialsrboxi:   
                                    initialsrboxi.selectedcol = 2
                                    initialsrboxi.turnwheeldown()
                                    initialsrboxi.rdict[initialsrboxi.selectedcol]["boxi"].draw()
                        else:
                            isaniover -=1
                            if isaniover < 1:
                                isanioverflag = True
                                if initialsrboxi:
                                    initialsrboxi.rdict[0]["boxi"].selected = False
                                    initialsrboxi.rdict[1]["boxi"].selected = False
                                    initialsrboxi.rdict[2]["boxi"].selected = True
                                    initialsrboxi.draw()
                        
                elif loadselection == True:
                    # This is the load screen showing part of the clock loop
                    if didishowloadscreen == False:
                        screen.fill(BLACK)
                        hscreen = boxi.boxi(screen, get_image("sharkhangar.png"), SCREEN_HEIGHT/2 - 512, SCREEN_WIDTH / 2 - 512, 3, GREEN, 3, YELLOW, 0, 0)

                        # Display Boxis for the list of savegames
                        scoreboxi = boxi.boxi(*boxidef1)
                        waveboxi = boxi.boxi(*boxidef2)
                        livesboxi = boxi.boxi(*boxidef3)
                        # This uses a default list of params above.  Long form it would be:
                        # textitemboxi = boxi.boxi(screen, textitem, 100, 400, 0, BLUE, 2, BLACK, 0, 0)
                        # Registering Boxi objects subscribes them for a redraw on refresh of the screen.
                        #scoreboxi.register()
                        #waveboxi.register()
                        #livesboxi.register()
                        # Column of savenames in Boxis, set up as a scrolling column.  This updates the boxis we created above.
                        savesc = boxi.cboxiscroll(*cboxiscdef1, displayboxi1 = scoreboxi, displaykey1 = "score", displayboxi2 = waveboxi, displaykey2 = "wave", displayboxi3 = livesboxi, displaykey3 = "lives", displayfont = font20, displaycolor = BLACK, tabord = 1)
                        
                        savesc.frame.bordercolor = boxi.gotfocuscolor
                        # And we register the new control
                        #savesc.register()  
                        jtimeout = 0                  
                        instboxi = boxi.boxi(screen, loadtextred, SCREEN_HEIGHT - 30, SCREEN_WIDTH / 2 - loadtextred.width / 2, 2, BLACK, 3, RED, 0, 0)    
                        didishowloadscreen = True
                        jtimeout = 1
                    # Look at every event in the queue
                    if savesc != None:
                        for event in pygame.event.get():
                            # Did the user hit a key or joystick button?
                            if nojoy != True:
                                if event.type == pygame.JOYBUTTONDOWN:
                                    if event.button == xbox360_controller.START:
                                        stuff = False                         
                                    if event.button == xbox360_controller.BACK:
                                        # Return to main screen
                                        didicleanup = False
                                        loadselection = False
                                        #running = False   
                                left_x, left_y = controller.get_left_stick()
                                if left_y > .2:
                                    if jtimeout < 1:
                                        savesc.updatebuttons(K_DOWN)
                                        jtimeout = 5
                                    if jtimeout > 0:
                                        jtimeout -=1        
                                elif left_y < -.2:
                                    if jtimeout < 1:
                                        savesc.updatebuttons(K_UP)
                                        jtimeout = 5
                                    if jtimeout > 0:
                                        jtimeout -=1  
                                triggers = controller.get_triggers()
                                buttons = controller.get_buttons()
                                if triggers > 0.3:
                                    stuff = False
                                if buttons[0] == 1:
                                    inits = savesc.cdict[savesc.selectedrow]["key"]
                                    readgamedict(initsuff = inits)
                                    loadgame = inits
                                    loaded = True    
                                    didicleanup = False
                                    loadselection = False 
                                    jtimeout = 5 
                                if buttons[2] == 1:
                                    stuff = False
                                if buttons[1] == 1:
                                    stuff = False
                                if buttons[3] == 1:
                                    stuff = False
                                if buttons[4] == 1:        
                                    stuff = False    
                            if event.type == KEYDOWN:
                                if event.key == K_RETURN:
                                    inits = savesc.cdict[savesc.selectedrow]["key"]
                                    readgamedict(initsuff = inits)
                                    loadgame = inits
                                    loaded = True    
                                    didicleanup = False
                                    loadselection = False
                        

                                elif event.key == K_ESCAPE:
                                    # Return to main screen
                                    didicleanup = False
                                    loadselection = False
                                elif event.key == K_DOWN or event.key == K_UP:
                                    savesc.updatebuttons(event.key)  
                            
                            if event.type == MOUSEBUTTONDOWN:
                                mousepos = pygame.mouse.get_pos()
                                boxi.mousehandler(event, event.button, mousepos)
                            if event.type == MOUSEWHEEL:
                                boxi.mousehandler(event, 0, (0, event.y)) 
                else:
                    # This is the Startup and Between Games part of the clock loop.
                    # Get rid of any remaining sprites except sunmoon and player
                    # Park on start screen
                    # If cleanup hasn't happened, clean up
                    if didicleanup == False:
                        #if initialsrboxi in locals(): del initialsrboxi
                        #if randomizeinitsboxibutton in locals(): del randomizeinitsboxibutton
                        #if savesc in locals(): del savesc 
                        #if scoreboxi in locals(): del scoreboxi
                        #if waveboxi in locals(): del waveboxi
                        #if livesboxi in locals(): del livesboxi
                        settingsscreen = False
                        loadselection = False
                        screen.fill(BLACK)
                        mscreen = boxi.boxi(screen, get_image("sharkcockpit.png"), SCREEN_HEIGHT/2 - 512, SCREEN_WIDTH / 2 - 512, 3, GREEN, 3, YELLOW, 0, 0)
                        pygame.mixer.music.stop()
                        for i, enemy1 in enumerate(enemies):
                            enemy1.kill()
                        for i, bullet1 in enumerate(bullets):
                            bullet1.kill()
                        for i, cloud1 in enumerate(clouds):
                            cloud1.kill()       
                        for i, mountain1 in enumerate(mountains):
                            mountain1.kill()
                        # Update highscore
                        if score > highscore:
                            highscore = score                      
                        loaddataexists = edict.loadgame()
                        # returns number of saved games
                        listsize = edict.loadgame()
                        # Add rendered versions of savenames to dictionary
                        # Add a dictionary key "render" containing renders of the text keys
                        renderedtext = boxi.rendertextdic(edict.savedict, font20, RED)
                                           
                        # Set Background for start screen     
                        #screen.fill((135, 206, 250))
                        texts3(highscore)
                        didicleanup = True
                    # Look at every event in the queue
                    for event in pygame.event.get():
                        # Did the user hit a key or joystick button?
                        if nojoy != True:
                            buttons = controller.get_buttons()
                            if buttons[2] == 1:
                                settingsscreen = True
                                settingssetup = False
                            if buttons[1] == 1:
                                loadselection = True
                                didishowloadscreen = False
                                #if loaddataexists > 0:
                                    #loaded = True                                        
                                    #screen.fill((135, 206, 250))
                                    #texts3(highscore)
                            if event.type == pygame.JOYBUTTONDOWN:
                                if event.button == xbox360_controller.START:
                                    # Press Enter to Play
                                    # Reinitialize gamestate at start
                                    initnewgame()
                                    ingame = True
                                    pause = False                           
                                if event.button == xbox360_controller.BACK:
                                    # Prepare for exit
                                    running = False           
                        if event.type == KEYDOWN:
                            if event.key == K_RETURN:
                                # Press Enter to Play
                                # Reinitialize gamestate at start
                                ingame = True
                                pause = False          
                                initnewgame()
                            elif event.key == K_ESCAPE:
                                # Prepare for exit
                                running = False               
                            #pressed_keysq = pygame.key.get_pressed()
                            
                            pressed_keys = pygame.key.get_pressed()
                            if pressed_keys[K_l] == True:
                                loadselection = True
                                didishowloadscreen = False
                            if pressed_keys[K_s] == True:                    
                                settingsscreen = True
                                settingssetup = False
                                #if loaddataexists > 0:
                                    #loaded = True                                        
                                    #screen.fill((135, 206, 250))
                                    #texts3(highscore)
                        # Did the user click the window close button? If so, stop the loop
                        elif event.type == QUIT:
                            running = False
                    # Draw Enter to Play, Esc to Exit, High Score
                    if playscreenupdated == False:
                        screen.fill(BLACK)
                        boxi.boxi(screen, get_image("sharkcockpit.png"), SCREEN_HEIGHT/2 - 512, SCREEN_WIDTH / 2 - 512, 3, GREEN, 3, YELLOW, 0, 0)                
                        # Set Background for start screen     
                        #screen.fill((135, 206, 250))
                        texts3(highscore)
                        playscreenupdated = True
                # Flip everything to the display
                pygame.display.flip()
                # Ensure we maintain a 30 frames per second rate
                clock.tick(30)
    except TypeError:
        print(entity.name)
        quit
#Save highscore
with open(hsfilename, "w") as file:
    file.write(str(highscore))
  
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
