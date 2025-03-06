# Written by Tom Maltby, credits follow
# www.maltby.org
# currently 1382 lines, 1 weekend of coding
# 
# Bassed off Jon Fincher's 120 line tutorial py_tut_with_images.py
# py_tut_with_images on github: https://github.com/realpython/pygame-primer/blob/master/py_tut_with_images.py
# Jon's blog: https://realpython.com/pygame-a-primer/
#
# Additional sounds from  http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
# # Arcade font from https://www.dafont.com/arcade-ya.font , by Yuji Adachi, listed as 100% free
#
# Barring 2 hours last summer, this is my first Python coding, and my first significant coding in any language
# in the last 15 years.  I'm sure it could be more elegant, but I'm having fun.
#
# Thanks to Jon and the creators of the great sounds and music
# Graphics except jet, missile, and white cloud are by me, using Corel and Gimp
 

# Import the pygame module
# Import random for random numbers
# Import os for file handling
# Import tkinter for root graphic context
# Import math for reasons
# Import glob for image preload

import random
import pygame
import tkinter
import os
import os.path
import math
import glob

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
)

# Define Colors
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")

# Define constants for the screen width and height
root = tkinter.Tk()
SCREEN_WIDTH = root.winfo_screenwidth() - 50
SCREEN_HEIGHT = root.winfo_screenheight() - 100
SCREEN_HEIGHT_NOBOX = SCREEN_HEIGHT - 100

# Define the Sun and Moon object
class SunMoon(pygame.sprite.Sprite):
    def __init__(self, wavenum):
        super(SunMoon, self).__init__()
        # Start with Sun loaded
        self.surf = get_image("sun1.png").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        # Place randomly
        self.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)

    def update(self, wavenum):

        if wavenum < 3:
            # Keep sun until wave 3
            self.surf = get_image("sun1.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if wavenum > 2 and wavenum < 4:
            # Then replace it with moon
            self.surf = get_image("moon1.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)

# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, firebullet):
        super(Player, self).__init__()
        self.surf = get_image("jet.png").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()
        # Start jet in middle of left edge
        self.rect.top = SCREEN_HEIGHT_NOBOX / 2
        self.rect.left = 30
        self.firebullet = 0
        self.hp = 100
        self.armor = 50

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if redflash == False and greenflash == False:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
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
            # Keep player on the screen if not on flash       
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT_NOBOX:
                self.rect.bottom = SCREEN_HEIGHT_NOBOX

# Define the mountain object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Mountain(pygame.sprite.Sprite):
    def __init__(self):
        super(Mountain, self).__init__()
        if wave < 3:
            self.mountnum = str(random.randint(1,2))
        elif wave < 5:
            self.mountnum = str(random.randint(1,4))
        else:
            self.mountnum = str(random.randint(1,6))
        self.surf = get_image("mountain" + self.mountnum + ".png").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # Starts on the bottom, off the screen to the right
        self.rect = self.surf.get_rect(bottomleft=(SCREEN_WIDTH + 30, SCREEN_HEIGHT_NOBOX),)
        if (random.randint(1,100) + (wave * wave)) > 90: 
                # Spawn gun on rock, more likely in later waves
                new_enemy = Enemy(7,14,1,self)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # Move the mountain based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        # if off left edge, kill
        if self.rect.right < 0:
            self.kill()

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, etype, boomcounter, hp, launcher):
        super(Enemy, self).__init__()
        if etype == 1:
            # Missile
            self.surf = get_image("missile.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL) 
            # Random speed, climb/dive               
            self.speed = random.randint(5, 20)
            self.climb = random.randint(-1,1)
            # Random start on right edge
            self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 20),random.randint(0, SCREEN_HEIGHT_NOBOX),))
            self.hp = 1
        elif etype == 3:
            # Homing missile from blimp
            self.surf = get_image("missile2.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # Just faster than blimp top speed
            self.speed = 12
            # Starts at nose of blimp
            self.rect = self.surf.get_rect(center=(launcher.rect.left - 20, launcher.rect.top))
            # Follows player on y axis
            if self.rect.top > player.rect.top:
                self.climb = - 3
            else:
                self.climb = 3
            self.hp = 1
        elif etype == 4:
            # Blimp
            self.surf = get_image("ship4.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # Random low speed, climb/dive                
            self.speed = random.randint(5, 10)
            self.climb = random.randint(-1,1)
            # Starts on right edge, random height
            self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 20),random.randint(0, SCREEN_HEIGHT_NOBOX),))
            # Takes 10 hits for blue blimp
            self.hp = 10
        elif etype == 5:
            # Armored blimp
            self.surf = get_image("ship4a.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL) 
            # Random low speed               
            self.speed = random.randint(5, 10)
            self.climb = random.randint(-1,1)
            # Starts on right edge, random height
            self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 20),random.randint(0, SCREEN_HEIGHT_NOBOX),))
            # Takes 20 hits for armored red blimp
            self.hp = 20
        elif etype == 7:
            # Gun on rock
            self.surf = get_image("gun1.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # Speed matches rocks, clouds
            self.speed = 5
            # Starts on top of rock
            self.rect = self.surf.get_rect(center = (launcher.rect.left, launcher.rect.top))
            self.rect.bottom = launcher.rect.top + 10
            self.rect.left = launcher.rect.left + 30
            self.hp = 25
        elif etype == 11:
            #extra life
            self.surf = get_image("extralife.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        elif etype == 12:
            #power up flamer
            self.surf = get_image("powerupflamer.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        elif etype == 13:
            #power up shock
            self.surf = get_image("powerupshock.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)            
        elif etype == 14:
            #power up bio
            self.surf = get_image("powerupbio.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        elif etype == 15:
            #power up pulse
            self.surf = get_image("poweruppulse.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        elif etype == 16:
            #power up health
            self.surf = get_image("poweruphealth.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
        elif etype == 17:
            #power up armor
            self.surf = get_image("poweruparmor.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
            
        if etype > 10 and etype < 20:
            # Power up on parachute
            # Random position at top, random side to side wobble, random slow drop
            self.speed = random.randint(-1,1)
            self.climb = random.randint(1,4)
            self.rect = self.surf.get_rect(center=(random.randint(100, SCREEN_WIDTH - 100),random.randint(-10, 0),))
        self.etype = etype
        # set blowup time to enemy as passed
        self.boomcounter = boomcounter

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        if random.randint(1,10)>5:
            if self.etype < 7 or self.etype > 7:
                self.climb = self.climb + random.randint(-1,1)
            if self.etype > 10:
                # Power up on parachute
                # Keep dropping slowly
                if self.climb < 1:
                    self.climb = 1
                elif self.climb > 4:
                    self.climb = 4
            if self.etype == 3:
                # Homing missile, adjust towards player
                if player.rect.top > self.rect.top:
                    self.climb = 3
                else:
                    self.climb = -3
        # Move, climb/dive
        if self.etype ==7:
            self.rect.move_ip(-self.speed, 0)
        else:
            self.rect.move_ip(-self.speed, self.climb)
        # Kill if offscreen
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > SCREEN_WIDTH + 100:
            self.kill()
        # Make top & bottom permeable to powerups; other enemies must stay in screen
        if self.rect.bottom > SCREEN_HEIGHT_NOBOX:
            if self.etype < 10:
                # Don't leave
                self.rect.bottom = SCREEN_HEIGHT_NOBOX
                if self.etype > 7 or self.etype < 7:
                    # Bounce
                    self.climb = -1 * self.climb
                # Explode missiles, blimps
                if self.etype == 1 or self.etype == 3:
                    self.etype = 2
                elif self.etype == 4 or self.etype ==5:
                    self.etype = 6
            elif self.rect.top > SCREEN_HEIGHT_NOBOX:
                self.kill
        if self.rect.top < 0:
            if self.etype < 10:
                # Don't leave
                self.top = 0
                # Bounce
                self.climb = -1 * self.climb
            elif self.rect.bottom < 0:
                self.kill()
        if self.etype == 4 or self.etype == 5 or self.etype == 7:
            # Functional blimp or gun
            if random.randint(1,100) + wave * 2 > 90:
                # Shoot homing missile, more likely in later waves
                new_enemy = Enemy(3,14,1,self)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
        if self.etype == 2:
            # Exploding missile
            # Decrement boomcounter to animate explosion
            self.boomcounter = self.boomcounter - 1
            if self.boomcounter > 8:
                self.surf = get_image("boom.png").convert()
            elif self.boomcounter < 9 and self.boomcounter > 5:
                self.surf = get_image("boom2.png").convert()
            elif self.boomcounter < 6:
                self.surf = get_image("boom3.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # If time's up, kill
            if self.boomcounter < 1:
                self.kill()
        if self.etype == 6:
            #Exploding Blimp
            # Decrement boomcounter to animate explosion
            self.boomcounter = self.boomcounter - 1
            if self.boomcounter > 8:
                self.surf = get_image("ship4xp1.png").convert()
            elif self.boomcounter < 9 and self.boomcounter > 5:
                self.surf = get_image("ship4xp2.png").convert()
            elif self.boomcounter < 6:
                self.surf = get_image("ship4xp3.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            # If time's up, kill
            if self.boomcounter < 1:
                self.kill()


# Define the bullet object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self,startx,starty,btype,boomcounter):
        super(Bullet, self).__init__()
        self.btype = btype
        if btype == 1:
            #Machine Gun
            self.surf = get_image("bullet.png") 
            self.speed = 25   
            shoot_sound.play()
        elif btype == 2:
            #Flamer
            self.surf = get_image("blast1.png")
            self.speed = 20
            self.boomcounter = boomcounter
            flamer_sound.play()
        elif btype == 3:
            #Shock Shield
            self.surf = get_image("shock1.png")
            self.speed = 0
            self.boomcounter = boomcounter
            shock_sound.play()
        elif btype == 4:
            #Bio Blaster
            self.surf = get_image("bio1.png")
            self.speed = 30
            self.boomcounter = boomcounter
            bio_sound.play()
        elif btype == 5:
            #Pulse
            self.surf = get_image("pulse1.png")
            self.speed = 15
            self.boomcounter = boomcounter
            pulse_sound.play()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        # The starting position is the nose of the plane
        self.rect = self.surf.get_rect(
            center=(
                startx,
                starty
            )
        )
        

    # Move the bullet based on speed
    # Remove it when it passes the right edge of the screen
    def update(self):
        
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.btype == 2:
            #Flamer
            self.boomcounter = self.boomcounter - 1
            if self.boomcounter > 22:
                self.surf = get_image("blast1.png")
            elif self.boomcounter < 23 and self.boomcounter > 16:
                self.surf = get_image("blast2.png")
            elif self.boomcounter < 17 and self.boomcounter > 10:
                self.surf = get_image("blast3.png")
            elif self.boomcounter < 11 and self.boomcounter > 5:
                self.surf = get_image("blast4.png")
            elif self.boomcounter < 6:
                self.surf = get_image("blast5.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill()
        if self.btype == 3:
            #Lightning Shield increments boomcounter instead of decrementing
            self.boomcounter = self.boomcounter + 1
            # If animation is finished, kill
            if self.boomcounter > 16:
                self.kill()
            if self.boomcounter < 5:
                self.surf = get_image("shock1.png")
            elif self.boomcounter > 4 and self.boomcounter < 9:
                self.surf = get_image("shock2.png")
            elif self.boomcounter > 8 and self.boomcounter < 13:
                self.surf = get_image("shock3.png")
            elif self.boomcounter > 12:
                self.surf = get_image("shock4.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
        if self.btype == 4:
            #Bio Spiral
            self.boomcounter = self.boomcounter - 1
            if self.boomcounter > 22:
                self.surf = get_image("bio1.png")
            elif self.boomcounter < 23 and self.boomcounter > 16:
                self.surf = get_image("bio2.png")
            elif self.boomcounter < 17 and self.boomcounter > 10:
                self.surf = get_image("bio3.png")
            elif self.boomcounter < 11 and self.boomcounter > 5:
                self.surf = get_image("bio4.png")
            elif self.boomcounter < 6:
                self.surf = get_image("bio5.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill() 
        if self.btype ==5:   
            #Pulse
            self.boomcounter = self.boomcounter - 1
            if self.boomcounter > 22:
                self.surf = get_image("pulse1.png")
            elif self.boomcounter < 23 and self.boomcounter > 16:
                self.surf = get_image("pulse2.png")
            elif self.boomcounter < 17 and self.boomcounter > 10:
                self.surf = get_image("pulse3.png")    
            elif self.boomcounter < 11 and self.boomcounter > 5:
                self.surf = get_image("pulse4.png")
            elif self.boomcounter < 6:
                self.surf = get_image("pulse5.png")
            self.surf.set_colorkey(WHITE, RLEACCEL)
            # If animation is finished, kill
            if self.boomcounter < 1:
                self.kill()   
        if self:
            center = self.rect.center
            self.rect = self.surf.get_rect()
            self.rect.center = center   

# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        if wave < 3:
            # During the day, use light clouds
            self.surf = get_image("cloud.png").convert()
        else:
            # At night, use dark clouds
            self.surf = get_image("cloud2.png").convert()
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
        self.rect.move_ip(-5, 0)
        # if off left edge, kill
        if self.rect.right < 0:
            self.kill()   

#Define and cache fonts
pygame.font.init()
font15 = pygame.font.Font("fonts/ARCADE_R.ttf", 15)
font16 = pygame.font.Font("fonts/ARCADE_R.ttf", 16)
font20 = pygame.font.Font("fonts/ARCADE_R.ttf", 20)
font30 = pygame.font.Font("fonts/ARCADE_R.ttf", 30)
font50 = pygame.font.Font("fonts/ARCADE_R.ttf", 50)
font60 = pygame.font.Font("fonts/ARCADE_R.ttf", 60)
font75 = pygame.font.Font("fonts/ARCADE_R.ttf", 75)

# Cache repeated text renders
playagametextblack = font30.render("Press Enter To Play - Press Esc to Quit", 1, BLACK)
playagametextred = font30.render("Press Enter To Play - Press Esc to Quit", 1, RED)
pausetext1 = font20.render("Controls:", 1, BLACK)
pausetext2 = font16.render("Flying: Arrow keys - Up, Down, Left, Right", 1, BLACK)
pausetext3 = font16.render("Weapons: Space - Machine Gun, X - Flamer, C - Shock Shield, V - Pulsar, B - Bio Blast", 1, BLACK)
pausetext4 = font16.render("Enter - Play / Pause / Unpause, Escape - Quit ", 1, BLACK)
pausetext5 = font20.render("Press Enter To UnPause - Press Esc to Quit", 1, BLACK)

def texts(lives, score):
    # gives lives, score, waves, high score
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",20)
    scoretext=font20.render("Lives:" + str(lives) + "  Score:" + str(score) +"  Wave: " + str(wave)+ ":" + "  (" + str(wavecounter) + "/" + str(wavegoal) + ")" +"   High Score: "+str(highscore), 1, (0,0,0))
    screen.blit(scoretext, (32, SCREEN_HEIGHT - 22))
    scoretext=font20.render("Lives:" + str(lives) + "  Score:" + str(score) +"  Wave: " + str(wave)+ ":" + "  (" + str(wavecounter) + "/" + str(wavegoal) + ")" +"   High Score: "+str(highscore), 1, (0,0,255))
    screen.blit(scoretext, (30, SCREEN_HEIGHT - 20))

def texts2(flamer, shock, bio, pulse):
    # gives ammo - machinegun has infinite ammo
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",15)
    scoretext=font15.render("MG(SP): 999   FLAMER(X): "+str(flamer)+"  SHOCK SHIELD(C): " + str(shock)  + "  PULSAR(V): " + str(pulse) + "   BIO BLAST(B): "+str(bio), 1, (0,0,0))
    screen.blit(scoretext, (32, SCREEN_HEIGHT - 42))
    scoretext=font15.render("MG(SP): 999   FLAMER(X): "+str(flamer)+"  SHOCK SHIELD(C): "+str(shock) + "  PULSAR(V): " + str(pulse) + "   BIO BLAST(B): "+str(bio), 1, (0,0,255))
    screen.blit(scoretext, (30, SCREEN_HEIGHT - 40))

def texts3(highscore):
    # on enter to play screen, gives high score
   # font = pygame.font.Font("fonts/ARCADE_R.ttf",30)
    
    #playagametext = font30.render("Press Enter To Play - Press Esc to Quit", 1, (0,0,0))
    ptxtoffset = playagametextblack.width / 2
    screen.blit(playagametextblack, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 60))
    #playagametext = font30.render("Press Enter To Play - Press Esc to Quit", 1, (255,0,0))
    screen.blit(playagametextred, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 - 58))
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",60)
    playagametext = font60.render("High Score: "+str(highscore), 1, (0,0,0))
    ptxtoffset = playagametext.width / 2
    screen.blit(playagametext, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 100))
    playagametext = font60.render("High Score: "+str(highscore), 1, (255,0,0))
    screen.blit(playagametext, (SCREEN_WIDTH / 2 - ptxtoffset + 2, SCREEN_HEIGHT / 2 + 102))
    #Control list
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",20)
    #pausetext1 = font20.render("Controls:", 1, (0,0,0))
    ptxtoffset = pausetext1.width / 2
    screen.blit(pausetext1, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2))
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",16)
    #pausetext2 = font16.render("Flying: Arrow keys - Up, Down, Left, Right", 1, (0,0,0))
    ptxtoffset = pausetext2.width / 2
    screen.blit(pausetext2, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 20))
    #pausetext3 = font16.render("Weapons: Space - Machine Gun, X - Flamer, C - Shock Shield, V - Pulsar, B - Bio Blast", 1, (0,0,0))
    ptxtoffset = pausetext3.width / 2
    screen.blit(pausetext3, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 40))
    #pausetext4 = font16.render("Enter - Play / Pause / Unpause, Escape - Quit ", 1, (0,0,0))
    ptxtoffset = pausetext4.width / 2
    screen.blit(pausetext4, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 60))

def texts4():
    #Pause screen    
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",20)
    #pausetext5 = font20.render("Press Enter To UnPause - Press Esc to Quit", 1, (0,0,0))
    ptxtoffset = pausetext5.width / 2
    screen.blit(pausetext5, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 - 30))
    #Control list
    #pausetext1 = font20.render("Controls:", 1, (0,0,0))
    ptxtoffset = pausetext1.width / 2
    screen.blit(pausetext1, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2))
    #font = pygame.font.Font("fonts/ARCADE_R.ttf",16)
    #pausetext2 = font16.render("Flying: Arrow keys - Up, Down, Left, Right", 1, (0,0,0))
    ptxtoffset = pausetext2.width / 2
    screen.blit(pausetext2, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 20))
    #pausetext3 = font16.render("Weapons: Space - Machine Gun, X - Flamer, C - Shock Shield, V - Pulsar, B - Bio Blast", 1, (0,0,0))
    ptxtoffset = pausetext3.width / 2
    screen.blit(pausetext3, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 40))
    #pausetext4 = font16.render("Enter - Play / Pause / Unpause, Escape - Quit ", 1, (0,0,0))
    ptxtoffset = pausetext4.width / 2
    screen.blit(pausetext4, (SCREEN_WIDTH / 2 - ptxtoffset, SCREEN_HEIGHT / 2 + 60))



def healthbar(left, top, health):
    healthbarborder = pygame.Rect(left + 40, top, 200, 30)
    healthbarfilled = pygame.Rect(left + 42, top + 2, int(196 * (health/100)), 26)
    heartimg = get_image("heart.png").convert()
    heartimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(heartimg, (left,top))

    if health > 70:
        healthbarcolor = GREEN
    elif health > 30:
        healthbarcolor = YELLOW
    else:
        healthbarcolor = RED
    pygame.draw.rect(screen, BLACK, healthbarborder, 0, 2)
    pygame.draw.rect(screen, healthbarcolor, healthbarfilled, 0, 2)

def armorbar(left, top, armor):
    armorbarborder = pygame.Rect(left + 40, top, 100, 30)
    armorbarfilled = pygame.Rect(left + 42, top +2, int(96 * (armor/50)), 26)
    shieldimg = get_image("shield.png").convert()
    shieldimg.set_colorkey(WHITE, RLEACCEL)
    screen.blit(shieldimg, (left, top))
    pygame.draw.rect(screen, BLACK, armorbarborder, 0, 2)
    pygame.draw.rect(screen, BLUE, armorbarfilled, 0, 2)

def statusdisplay():
    statusbox = pygame.Rect(3, SCREEN_HEIGHT - 94, SCREEN_WIDTH - 3, 94)
    statusboxframe = pygame.Rect(0,SCREEN_HEIGHT - 100,SCREEN_WIDTH,100)
    pygame.draw.rect(screen, BLUE, statusboxframe, 0, 3)
    pygame.draw.rect(screen, GRAY, statusbox, 0, 3)   
    # Draw our game text
    texts(plives, score)
    texts2(flamer,shock,bio,pulse)   
    healthbar(10, SCREEN_HEIGHT - 80, player.hp)
    armorbar(250, SCREEN_HEIGHT - 80, player.armor)    
# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()



# Create the screen object
# First set the icon
icon = pygame.image.load("Graphics/""icon.png")
icon.set_colorkey(BLACK, RLEACCEL)
pygame.display.set_icon(icon)
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('They Comin')

# Preload graphics
def get_image(key):
    if not key in image_cache:
        image_cache[key] = pygame.image.load("Graphics/" + key).convert()
    return image_cache[key]

image_cache = {}
images = glob.glob ("Graphics/*.png")
for image in images:
    img_name = os.path.basename(image)
    get_image(img_name)

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
pygame.time.set_timer(ADDMOUNTAIN, 2000)
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

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
# Many new additional sounds sourced from: http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds/Falling_putter.ogg")
shoot_sound = pygame.mixer.Sound("sounds/Shoot.ogg")
collision_sound = pygame.mixer.Sound("sounds/Small_explosion.ogg")
bio_sound = pygame.mixer.Sound("sounds/Bio_splat.ogg")
shock_sound = pygame.mixer.Sound("sounds/Shock_sound2.ogg")
flamer_sound = pygame.mixer.Sound("sounds/Flamer_sound.ogg")
powerup_sound = pygame.mixer.Sound("sounds/Power_up.ogg")
wavechange_sound = pygame.mixer.Sound("sounds/Wave_change.ogg")
pulse_sound = pygame.mixer.Sound("sounds/Pulse_sound.ogg")

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

# Set player lives, score, special weapons, redflash, greenflash, gamerunning variables
plives = 3
score = 0
flamer = 100
shock = 100
bio = 100
pulse = 100
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
wavegoal = 50
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

# Variable to keep our main loop running - false is exit condition
running = True

# Our main loop
while running:
    if pause == True and ingame == True:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    # Press Enter to Play
                    # unpause
                    pause = False
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
        texts4()
        pygame.display.flip()
    else:
        if ingame:
            #pressed_keysq = pygame.key.get_pressed()
            #if pressed_keysq == K_p:
            #    pause = True
            # Look at events relative to pause status
            for event in pygame.event.get():
            # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop
                    if event.key == K_ESCAPE:
                        ingame = False        
                        for i, enemy1 in enumerate(enemies):
                            enemy1.kill()
                        for i, bullet1 in enumerate(bullets):
                            bullet1.kill()
                        for i, cloud1 in enumerate(clouds):
                            cloud1.kill()                
                        for i, mountain1 in enumerate(mountains):
                            mountain1.kill()
                    elif event.key == K_RETURN:
                        pause = True
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
                    # No new enemies while dead/wave 'Get Ready'
                    wavcompleteperc = int(((wavecounter + wave)/wavegoal) * 100)
                    if random.randint(1,100) < wavcompleteperc + 25 + wave * wave:
                        enemiestocreate = random.randint(1,int(math.sqrt(wave)))
                        for x in range(1, enemiestocreate + 1):
                            if redflash == False and greenflash == False:
                                # Create the new enemy, and add it to our sprite groups
                                hp = 1
                                powerup = random.randint(1,100)
                                if powerup < 3 + wave :
                                    # Blimp1
                                    newetype = 4
                                    hp = 10
                                if powerup > 2 + wave and powerup < 5 + wave * 2:
                                    # Blimp2
                                    newetype = 5
                                    hp = 20
                                if powerup < 88 and powerup > 4 + wave * 2:
                                    # Missile
                                    newetype = 1
                                elif powerup > 86 and powerup < 89:
                                    # Health
                                    newetype = 16
                                elif powerup > 88 and powerup < 91:
                                    # Armor
                                    newetype = 17
                                elif powerup > 90 and powerup < 93:
                                    # Extra Life
                                    newetype = 11
                                elif powerup > 92 and powerup < 95:
                                    # Power Up FLamer
                                    newetype = 12
                                elif powerup > 94 and powerup < 97:
                                    # Power Up Shock
                                    newetype = 13
                                elif powerup > 96 and powerup < 99:
                                    # Power Up Bio
                                    newetype = 14
                                elif powerup > 97:
                                    # Power Up Pulse
                                    newetype = 15
                                new_enemy = Enemy(newetype,14,hp,0)
                                enemies.add(new_enemy)
                                all_sprites.add(new_enemy)

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
                        new_bullet = Bullet(player.rect.right,player.rect.top,1,8)
                        bullets.add(new_bullet)
                        all_sprites.add(new_bullet)
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
                            new_bullet = Bullet(player.rect.right - player.rect.width/2, player.rect.top + player.rect.height/2,3,0)      
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
            enemies.update()
            bullets.update()
            #player.update(pressed_keys)
            clouds.update()
            
            # Draw all our sprites
            screen.blit(wavesunmoon.surf, wavesunmoon.rect)
            screen.blit(player.surf, player.rect)
            for entity in mountains:
                screen.blit(entity.surf, entity.rect)
            for entity in enemies:
                screen.blit(entity.surf, entity.rect)
            for entity in bullets:
                screen.blit(entity.surf, entity.rect)
            for entity in clouds:
                screen.blit(entity.surf, entity.rect)
            
            #for entity in all_sprites:
            #    screen.blit(entity.surf, entity.rect)
            # Draw our status box, add texts
            statusdisplay()
            
            if redflash:
                pygame.mixer.music.stop()
                #Count down on get ready message - has to occur after sprites
                counterstr = ""
                #font = pygame.font.Font("fonts/ARCADE_R.ttf",30)
                deadtext = font30.render("You Died!  Lives remain: " + str(plives), 1, BLACK)
                dtxtoffset = deadtext.width / 2
                screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset, 200))
                deadtext = font30.render("You Died!  Lives remain: " + str(plives), 1, BLUE)
                screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset + 2, 202))
                # Bigger font for the countdown
                #font = pygame.font.Font("fonts/ARCADE_R.ttf",75) 
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
                #font = pygame.font.Font("fonts/ARCADE_R.ttf",30)
                deadtext = font30.render("Wave #" + str(wave) + " (0/" +str(wavegoal) + ")", 1, BLACK)
                dtxtoffset = deadtext.width / 2
                screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset, 200))
                deadtext = font30.render("Wave #" + str(wave) + " (0/" +str(wavegoal) + ")", 1, BLUE)
                screen.blit(deadtext, (SCREEN_WIDTH / 2 - dtxtoffset + 2, 202))
                # Bigger font for the countdown
                #font = pygame.font.Font("fonts/ARCADE_R.ttf",75) 
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
                    enemy1.boomcounter = 10
                    if enemy1.etype == 1 or enemy1.etype == 3:
                        # If missile, make exploding missile
                        enemy1.etype = 2
                    elif enemy1.etype > 3 and enemy1.etype < 6:
                        # If blimp, make exploding blimp
                        enemy1.etype = 6
                    elif enemy1.etype == 7:
                        enemy1.kill()
                    elif enemy1.etype > 10:
                        enemy1.kill()
                    score = score + 1
                    wavecounter = wavecounter + 1
                # If no lives remain, kill player
                if plives < 1:
                    # Go to start screen
                    ingame = False

            # Check if any enemies have collided with the player
            crash = pygame.sprite.spritecollideany(player, enemies)
            if crash:
                if crash.etype < 10:
                    # Missile or blimp, possibly exploding
                    collision_sound.play()
                    # Implement variable damage
                    if crash.etype == 1:
                        # Missile
                        damage = random.randint(15, 35)
                    elif crash.etype == 2:
                        # Exploding Missile
                        damage = random.randint(1, 20)
                    elif crash.etype == 3:
                        # Homing Missile
                        damage = random.randint(25, 45)
                    elif crash.etype == 4:
                        # Blimp
                        damage = random.randint(50, 75)
                    elif crash.etype == 5:
                        # Armored Blimp
                        damage = random.randint(75, 125)
                    elif crash.etype == 6:
                        # Exploding Blimp
                        damage = random.randint(25, 50)
                    elif crash.etype == 7:
                        # Gun
                        damage = random.randint(25, 30)
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
                            enemy1.boomcounter = 10
                            if enemy1.etype == 1 or enemy1.etype == 3:
                                # If missile, make exploding missile
                                enemy1.etype = 2
                            elif enemy1.etype > 3 and enemy1.etype < 6:
                                # If blimp, make exploding blimp
                                enemy1.etype = 6
                            elif enemy1.etype == 7:
                                enemy1.kill()
                            score = score + 1
                            wavecounter = wavecounter + 1
                        # If no lives remain, kill player
                        if plives < 1:
                            # Go to start screen
                            ingame = False
                
                elif crash.etype == 11:
                    # Extra Life
                    plives = plives + 1
                elif crash.etype == 12:
                    # Power Up Flamer
                    flamer = flamer + 100
                elif crash.etype == 13:
                    # Power Up Shock
                    shock = shock + 100
                elif crash.etype == 14:
                    # Power Up Bio
                    bio = bio + 100
                elif crash.etype == 15:
                    # Power Up Pulsar
                    pulse = pulse + 100
                elif crash.etype == 16:
                    # Power Up Health
                    player.hp = player.hp + 50
                    if player.hp > 100:
                        player.hp = 100
                elif crash.etype == 17:
                    # Power Up Armor
                    player.armor = player.armor + 25
                    if player.armor > 50:
                        player.armor = 50

                # Remove the Enemy
                crash.kill()
                # Stop any moving sounds and play the collision sound
                move_up_sound.stop()
                move_down_sound.stop()
                if crash.etype < 10:
                    # If hostile
                    collision_sound.play()
                elif crash.etype > 10:
                    # If powerup
                    score = score + 25
                    wavecounter = wavecounter + 1
                    powerup_sound.play()
            # Check for other collisions, kill colliding enemies and destructable bullets   
            for i, enemy1 in enumerate(enemies):
                enemy2 = pygame.sprite.spritecollideany(enemy1, enemies)
                # If enemies collide
                if enemy2 != enemy1:
                    # Not with themselves
                    if enemy2.etype > 10 and enemy1.etype > 10:
                        # If 2 powerups, separate
                        if enemy2.rect.left < enemy1.rect.left:
                            enemy2.rect.left = enemy2.rect.left -25
                            enemy1.rect.left = enemy1.rect.left +25
                        else:
                            enemy2.rect.left = enemy2.rect.left +25
                            enemy1.rect.left = enemy1.rect.left -25
                    if enemy2.etype == 1 or enemy2.etype == 3:
                        # If missile, make exploding missile
                        enemy2.etype = 2
                        score = score + 1
                    elif enemy2.etype > 3 and enemy2.etype < 6:
                        # If blimp, damage blimp
                        enemy2.hp = enemy2.hp - 1
                        # If blimp out of hp, make exploding blimp
                        if enemy2.hp < 1:
                            score = score + 5
                            enemy2.etype = 6
                    elif enemy2.etype == 7:
                        # If gun, damage gun
                        enemy2.hp = enemy2.hp - 1
                        if enemy2.hp < 1:
                            score = score + 50
                            enemy2.kill()
                    else: 
                        # If powerup hit enemy, kill powerup
                        enemy2.kill()
                    if enemy1.etype == 1 or enemy1.etype == 3:
                        # If missile, make expliding missile
                        enemy1.etype = 2
                        score = score + 1
                    elif enemy1.etype > 3 and enemy1.etype < 6:
                        # If blimp, damage blimp
                        enemy1.hp = enemy1.hp - 1
                        # If blimp out of hp, make exploding blimp
                        if enemy1.hp < 1:
                            score = score + 5
                            enemy1.etype = 6
                    elif enemy2.etype == 7:
                        # If gun, damage gun
                        enemy2.hp = enemy2.hp - 1
                        if enemy2.hp < 1:
                            score = score + 10
                            enemy2.kill()
                    else:
                        # If powerup hit enemy, kill powerup
                        enemy1.kill()
                    collision_sound.play()
                    wavecounter = wavecounter + 2
            for i, thisenemy in enumerate(enemies):
                bullethit = pygame.sprite.spritecollideany(thisenemy, bullets)
                # If bullet hits enemy
                if bullethit:
                    collision_sound.play()
                    if thisenemy.etype == 1 or thisenemy.etype == 3:
                        # If missile, make exploding missile
                        thisenemy.etype = 2
                        score = score + 1
                        wavecounter = wavecounter + 1
                        if bullethit.btype == 1:
                            # MG bullets go away on impact
                            bullethit.kill()
                    elif thisenemy.etype == 4 or thisenemy.etype == 5:
                        # If blimp, damage blimp
                        thisenemy.hp = thisenemy.hp - 1
                        # If blimp out of hp, make exploding blimp
                        if thisenemy.hp < 1:
                            thisenemy.etype = 6
                            score = score + 5
                            wavecounter = wavecounter + 1
                        if bullethit.btype == 1:
                            # MG bullets go away on impact
                            bullethit.kill()
                    elif thisenemy.etype == 7:
                        # If gun, damage gun
                        thisenemy.hp = thisenemy.hp - 1
                        if thisenemy.hp < 1:
                            score = score + 10
                            thisenemy.kill()
                        if bullethit.btype == 1:
                            # MG bullets go away on impact
                            bullethit.kill()
            for i, thismountain in enumerate(mountains):
                bullethit = pygame.sprite.spritecollideany(thismountain, bullets)
                if bullethit:
                    if bullethit.btype == 1:
                        bullethit.kill()
                    else:
                        if bullethit.boomcounter > 2:
                            bullethit.boomcounter = 2
                        
            for i, thismountain in enumerate(mountains):
                enemyhit = pygame.sprite.spritecollideany(thismountain, enemies)
                if enemyhit:
                    if enemyhit.etype > 7 or enemyhit.etype < 7:
                        if enemyhit.etype == 1 or enemyhit.etype == 3:
                            enemyhit.etype = 2
                            enemyhit.boomcounter = 3
                        if enemyhit.etype == 4 or enemyhit.etype == 5:
                            enemyhit.etype = 6
                        score = score + 1
            if wavecounter > wavegoal:
                # Set up next wave
                wave = wave + 1
                wavegoal = wavegoal + (wave * wave * 10) + 100
                wavecounter = 0
                # Green flash for wave complete
                greenflash = True
                greenflashticks = pygame.time.get_ticks()
                move_up_sound.stop()
                move_down_sound.stop()
                wavechange_sound.play()
                # Move player positon to hide
                player.rect.left = -300
                player.rect.top = SCREEN_HEIGHT_NOBOX / 5
                # update sunmoon state & new random position
                wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
                wavesunmoon.update(wave)
                # Cause destruction event for any remaining enemies
                for i, enemy1 in enumerate(enemies):
                    enemy1.boomcounter = 10
                    if enemy1.etype == 1 or enemy1.etype == 3:
                        # If Missile, make exploding missile
                        enemy1.etype = 2
                        score = score + 1
                    if enemy1.etype == 4 or enemy1.etype ==5:
                        # If Blimp, make exploding blimp
                        enemy1.etype = 6
                        score = score + 5
                    if enemy1.etype == 7:
                        #if Gun, kill
                        enemy1.kill()
                    if enemy1.etype > 10:
                        # If Powerup, kill
                        enemy1.kill()
                    wavecounter = wavecounter + 1

            if score > highscore:
                highscore = score
            # Flip everything to the display
            pygame.display.flip()
            # Ensure we maintain a 30 frames per second rate
            clock.tick(30)
        else:
            # Get rid of any remaining sprites except sunmoon and player
            # Park on start screen
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
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        # Press Enter to Play
                        # Reinitialize gamestate at start
                        ingame = True
                        pause = False
                        plives = 3
                        score = 0
                        flamer = 100
                        shock = 100
                        bio = 100
                        pulse = 100
                        wave = 1
                        redflash = False
                        greenflash = False  
                        wavecounter = 0
                        wavegoal = 150
                        pygame.mixer.music.play(loops=-1)
                        wavesunmoon.rect.center=(random.randint(100, SCREEN_WIDTH),random.randint(0, SCREEN_HEIGHT_NOBOX),)
                        wavesunmoon.update(wave)
                        player.rect.left = 30
                        player.rect.top = SCREEN_HEIGHT_NOBOX / 5

                    elif event.key == K_ESCAPE:
                        # Prepare for exit
                        running = False               
                    pressed_keysq = pygame.key.get_pressed()
                # Did the user click the window close button? If so, stop the loop
                elif event.type == QUIT:
                    running = False
            # Set Background for start screen     
            screen.fill((135, 206, 250))
            # Draw Enter to Play, Esc to Exit, High Score
            texts3(highscore)
            # Flip everything to the display
            pygame.display.flip()
            # Ensure we maintain a 30 frames per second rate
            clock.tick(30)
#Save highscore
with open(hsfilename, "w") as file:
    file.write(str(highscore))
  
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
