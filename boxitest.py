# Test surface for boxi.py
# (c)Tom Maltby 2025
#
# This is a test surface to display some sample BoxyPyg controls.  It demonstrates usage, declarations, animation handling, etc.
#
# The BoxiPyg project is an opensource UI contstruction toolkit library.  It leverages class inheritance from a basic Boxi object
# consisting of three pygame.rect objects and some associated properties and methods to quickly create new custom controls for your 
# projects.  It does not yet have a WYSIWYG abstraction layer or a wiki for documentation, however once I add a few more sample
# controls, these additions are planned.
#
# Usage is free under the MIT license, just please credit me in your project.  I hope it brings general satisfaction and quick
# versatile customization to your work in Pygame.
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
#
#  If you want to learn about the use of Boxis, defaults are set around line 140, and calls to the library start around line 190.
#  Until that point we are including, loading resources to display, setting up screens, delaring fonts, colors, etc.
#
#  The code is thoughtfully commented, but some users may want to wait until a more comprehensive documentation wiki takes shape.  This 
#  is an ongoing project, and I want to bang out several more advanced controls for a screen or two of good looking solid functioning
#  demonstration purposes before I build a big wiki.  Right now my time is better spent expanding and commenting.

# Import and initialize the pygame library
import pygame
# Import boxi
import boxi
# Import edict for sample data
import edict
# Import xbox360_controller
import xbox360_controller
# Import glob for direct -> dictionary usage
import glob
# Iomport os for files
import os
# This library is really useful for controlling what screen size you wind up measuring
# Boxi has no unique need for it, but it is part of my standard environment pack
from screeninfo import get_monitors
# Import random for random numbers
import random
# Import mouse
import pygame.mouse

# Initialize lists for monitor detection / setup
screen_nums = []
screen_positions = []
screen_sizes = []

def getscreensandsizes():
    # This function keeps us from accidentally spreading across multiple monitors
    screen_num = 0
    for m in get_monitors():       
        print(str(m))
        # Access individual attributes
        print(f"Monitor name: {m.name}")
        print(f"Position: x={m.x}, y={m.y}")
        print(f"Size: width={m.width}, height={m.height}")
        print(f"Is primary: {m.is_primary}")
        screen_nums.append(screen_num)
        screen_positions.append((m.x,m.y))
        screen_sizes.append((m.width,m.height))
        screen_num += 1
    return m

# Define constants for the screen width and height
scnums = getscreensandsizes()

SCREEN_WIDTH = int(screen_sizes[0][0]) 
SCREEN_HEIGHT = int(screen_sizes[0][1])   
SCREEN_HEIGHT_NOBOX = SCREEN_HEIGHT - 100
# Setup the window we'll use for drawing
screen = pygame.display.set_mode([800, 800])

boxi.screensetup(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT_NOBOX)

from pygame.locals import (
    K_ESCAPE, #Quit
    K_TAB, #Tab between controls
    K_RSHIFT, # For reverse direction of tab through focus
    K_LSHIFT, # For reverse direction of tab through focus
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
    MOUSEBUTTONDOWN,
    MOUSEWHEEL,
    MOUSEBUTTONUP,
    MOUSEMOTION
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

pygame.init()

pygame.font.init()
font15 = pygame.font.Font("fonts/arcade_r.ttf", 15)
font16 = pygame.font.Font("fonts/arcade_r.ttf", 16)
font20 = pygame.font.Font("fonts/arcade_r.ttf", 20)
font30 = pygame.font.Font("fonts/arcade_r.ttf", 30)
font50 = pygame.font.Font("fonts/arcade_r.ttf", 50)
font60 = pygame.font.Font("fonts/arcade_r.ttf", 60)
font75 = pygame.font.Font("fonts/arcade_r.ttf", 75)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

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

# Animation timers
isanioverflag = True
isaniover = 0

dispstr = "This is a big text string, such as I would use for plot dumps, conversations, etc.  It should be evealuated by control width and font size, and fed into a scrolling multiline display.  The last noble Assault Shark pilot perserveres in their daily struggle aginst the sky jet minions and their kleptofacist groundling artillery support."

# Preload graphics - called by image cache for all pngs in the graphics directory
def get_image(key):
    if not key in image_cache:
        image_cache[key] = pygame.image.load("graphics/" + key).convert()
    return image_cache[key]

# Set some Boxi defaults to pass with *parameters

# First stuff for them to hold

# This creates a key of a rendering of the text of primary key in the dictionary to be sorted
# returns number of saved games
listsize = edict.loadgame()
# Add rendered versions of savenames to dictionary
# Add a dictionary key "render" containing renders of the text keys
renderedtext = boxi.rendertextdic(edict.savedict, font20, RED)
# A larger dict file for comparison
renderedtext2 = boxi.rendertextdic(edict.enemydict, font20, RED)

# A default rendered text item to display in a Boxi
textitem = font20.render("A text object", 1, BLACK)

# Initials defaults
initialfont = font50
initialfcolor = BLACK
# Dictionary for initial wheel positions
rendera = initialfont.render("A", 1, initialfcolor)
initialsdef = {1: {"lit": "A", "ren": rendera, "val": 65}, 2: {"lit": "A", "ren": rendera, "val": 65}, 3:{"lit": "A", "ren": rendera, "val": 65}}
# Programatically make an allowable ascii dictionary
initialspos = {}
ctr = 65 # Ascii value of "A" - capitals are 65 to 90, numbers are 48 to 57, but we want the numbers to appear after the letters
while ctr < 91:
    initialspos [ctr] = {"lit": chr(ctr), "ren": initialfont.render(chr(ctr), 1, initialfcolor)}
    ctr += 1
ctr = 48
while ctr < 58:
    initialspos [ctr] = {"lit": chr(ctr), "ren": initialfont.render(chr(ctr), 1, initialfcolor)}
    ctr += 1

# Now parameter lists for *params...
# parameters for default boxi call with rendered text object - these will be extra field displays for the savegame Cboxiscroll
boxidef1 = (screen, textitem, 30, 500, 0, LIGHTBLUE, 2, BLACK, 0, 0)
boxidef2 = (screen, textitem, 60, 500, 0, LIGHTBLUE, 2, BLACK, 0, 0)
boxidef3 = (screen, textitem, 90, 500, 0, LIGHTBLUE, 2, BLACK, 0, 0)
# parameters for a scrolling column of boxes, dictionary driven, with linked fields by key displayed
cboxiscdef1 = (screen, renderedtext, "render", 160, 510, 1, WHITE, 1, BLUE, 0, 0, 7)

# parameters for the rboxipicwheels row for entering three initials video game style
# initialspos{} is the dictionary of options per wheel, with the ascii character literal and its rendering for
# all allowable ascii characters.  initialsdef{} is the default values of A, A, A.
initrboxidef = (screen, initialsdef, "ren", 100, 220, 3, YELLOW, 2, BLACK, initialspos, 0, 0)


image_cache = {}
# Gets a list of all images in the graphics directory
images = glob.glob ("graphics/*.png")
# Loads all images into the image_cache dictionary
for image in images:
    img_name = os.path.basename(image)
    get_image(img_name)

# Preload JSON enemies
jsons = edict.addjsons()
print(str(jsons) + " JSON file(s) added")

# Small dictionary of pictures
item = get_image("shell3.png")
item2 = get_image("shell3b.png")
item3 = get_image("shell3c.png")
shells = {
    1: {"image": item,
    },
    2: {"image": item2,
    },
    3: {"image": item3,
    }
}

# White screen surface
screen.fill((255, 255, 255))

# Not setup yet, runs the setup when the running loop begins
issetup = False

# Run until the user asks us to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        # Consistent objects go here
        # Initialize some boxis
        # Only run setup once
        if issetup == False:
            # Display Boxis for the list of savegames
            scoreboxi = boxi.boxi(*boxidef1)
            waveboxi = boxi.boxi(*boxidef2)
            livesboxi = boxi.boxi(*boxidef3)
            # This uses a default list of params above.  Long form it would be:
            # textitemboxi = boxi.boxi(screen, textitem, 100, 400, 0, BLUE, 2, BLACK, 0, 0)
            # Registering Boxi objects subscribes them for a redraw on refresh of the screen.
            scoreboxi.register()
            waveboxi.register()
            livesboxi.register()
            # Column of savenames in Boxis, set up as a scrolling column.  This updates the boxis we created above.
            savesc = boxi.cboxiscroll(*cboxiscdef1, displayboxi1 = scoreboxi, displaykey1 = "score", displayboxi2 = waveboxi, displaykey2 = "wave", displayboxi3 = livesboxi, displaykey3 = "lives", displayfont = font20, displaycolor = BLACK, tabord = 1 )
            # And we register the new control
            savesc.register()
            # rboxi for initials
            initialsrboxi = boxi.rboxipicwheels(*initrboxidef, tabord = 2)
            # And we register the new control
            initialsrboxi.register()
            # Boxibutton for randomizing initials - this passes a function hook for the button pressed event
            randomizeinitsboxibutton = boxi.boxibutton(150, 50, 100, 30, 3, YELLOW, 1, BLACK, randomizebutton, 5, "Randomize Initials", screen)
            # And we register the new control
            randomizeinitsboxibutton.register()
            # Column of Boxis with pictures of a shell enemy
            shellsc = boxi.cboxi(screen, shells, "image", 40, 40, 1, BLACK, 1, RED,0,0, tabord = 3)
            # Register for redraw events
            shellsc.register()
            # This row of boxis is not registered and will be covered by the timer based screen fill event.  
            # Other controls will be redrawn if they have called their register method.
            somerboxi = boxi.rboxi(screen, shells, "image", 600, 50, 1, BLACK, 1, RED,0,0, tabord = 4)
            somerboxi.register()
            # skip setup in future
            issetup = True
        # Always recognize the close program button
        if event.type == pygame.QUIT:
            running = False
        # Joystick events
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == xbox360_controller.START:
                pause = False
                #pygame.mixer.music.play(loops=-1)
            if event.button == xbox360_controller.BACK:
                ingame = False
        # Keyboard events
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                stuff = False
            if event.key == K_TAB:
                # Switch through controls according to tab order
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_RSHIFT] == True or pressed_keys[K_LSHIFT] == True:
                    boxi.tabcontrols(False) # Shift-Tab goes back in taborder
                else:
                    boxi.tabcontrols(True) # True sets forward: Tab w/o Shift
                # Iterate tab order
            # See if a control has focus, and if so if it has registered for the event.key
            # If it has registered the keystroke and has focus, deliver the keystroke to the control. 
            if boxi.currentfocuscontrol:
                if boxi.regbuttons[boxi.currentfocustab]:
                    if event.key in boxi.regbuttons[boxi.currentfocustab]["buttons"]:
                        boxi.currentfocuscontrol.updatebuttons(event.key)
            if event.key == K_DOWN:
                stuff = False
            if event.key == K_UP:
                stuff = False
            if event.key == K_RIGHT:
                stuff = False
            if event.key == K_LEFT:
                stuff = False
        if event.type == MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            boxi.mousehandler(event, event.button, mousepos)
        if event.type == MOUSEWHEEL:
            boxi.mousehandler(event, 0, (0, event.y))
        if event.type == MOUSEBUTTONUP:
            # This unshadows any buttons that were in a pressed/shadowed state
            for control in boxi.regcontrols:
                if hasattr(control, "pressedshadow") and control.pressedshadow == True:
                    control.rectborder.top = control.rectbox.top 
                    control.rectborder.left = control.rectbox.left 
                    control.draw()

    # This line - boxi.drawregcontrols() - causes registered controls to be redrawn - right now not needed, 
    # but included as a comment so that it can be applied as desired.
    #boxi.drawregcontrols()
    # This is an animation handler for the initials rboxi's randomize initials function, called by the rboxi button above.
    # It serves no vital purpose, but displays the scrolling of the initials as if it were a slot machine, which is fun.
    if a1 > 0 or a2 > 0 or a3 > 0:
        isanioverflag = False
        isaniover = 3
        if a1 > 0:
            a1 -= 1
            initialsrboxi.selectedcol = 0
            initialsrboxi.turnwheeldown()
            initialsrboxi.rdict[initialsrboxi.selectedcol]["boxi"].draw()
        if a2 > 0:
            a2 -= 1
            initialsrboxi.selectedcol = 1
            initialsrboxi.turnwheeldown()
            initialsrboxi.rdict[initialsrboxi.selectedcol]["boxi"].draw()
        if a3 > 0:
            a3 -= 1
            initialsrboxi.selectedcol = 2
            initialsrboxi.turnwheeldown()
            initialsrboxi.rdict[initialsrboxi.selectedcol]["boxi"].draw()
    else:
        isaniover -=1
        if isaniover < 1:
            isanioverflag = True
            initialsrboxi.rdict[0]["boxi"].selected = False
            initialsrboxi.rdict[1]["boxi"].selected = False
            initialsrboxi.rdict[2]["boxi"].selected = True
            initialsrboxi.draw()

    clock.tick(30)

    # Flip the display
    pygame.display.flip()

# We're done, so we can quit now.
pygame.quit()
