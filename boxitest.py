# Test surface for boxi.py
# Tom Maltby 2025
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
# This is really useful for controlling what screen size you wind up measuring
from screeninfo import get_monitors

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
scnums = getscreensandsizes()

SCREEN_WIDTH = int(screen_sizes[0][0])  #root.winfo_screenwidth() # - 50
SCREEN_HEIGHT = int(screen_sizes[0][1])   #root.winfo_screenheight() # - 100
SCREEN_HEIGHT_NOBOX = SCREEN_HEIGHT - 100
# Setup the window we'll use for drawing
screen = pygame.display.set_mode([800, 800])

boxi.screensetup(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT_NOBOX)

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
)



# Define Colors
RED = pygame.Color("red")
BLUE = pygame.Color("blue")
GREEN = pygame.Color("green")
GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
YELLOW = pygame.Color("yellow")

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

# Cache repeated text renders

# Preload graphics
def get_image(key):
    if not key in image_cache:
        image_cache[key] = pygame.image.load("graphics/" + key).convert()
    return image_cache[key]

# Set some Boxi defaults to pass with *parameters

renderedtext = boxi.rendertextdic(edict.enemydict, font20, RED)

textitem = font20.render("A text object", 1, BLACK)
# parameters for default boxi call with rendered text object
boxidef1 = (screen, textitem, 100, 400, 0, BLUE, 2, BLACK, 0, 0)
# parameters for a scrolling column of boxes, dictionary driven, with linked fields by key displayed
cboxiscdef1 = (screen, renderedtext, "render", 300, 400, 1, WHITE, 1, BLUE, 0, 0, 7)


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

invent = {
    "arrows:": 30,
    "torches": 5,
    "gp:": 37
}


item = get_image("shell3c.png")
shells = {
    1: {"image": item,
    },
    2: {"image": item,
    },
    3: {"image": item,
    }
}
#savenamesc = {}
#shellsc = {}
# returns number of saved games
listsize = edict.loadgame()
# Add rendered versions of savenames to dictionary
# Add a dictionary key "render" containing renders of the text keys
#renderedtext = boxi.rendertextdic(edict.savedict, font20, RED)
# A larger dict file for comparison
renderedtext = boxi.rendertextdic(edict.enemydict, font20, RED)


screen.fill((255, 255, 255))
issetup = False
# Run until the user asks us to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        # Fill the background with white
        # Consistent objects go here
        # Initialize some boxis
        if issetup == False:
            # Demo text boxi
            textitemboxi = boxi.boxi(*boxidef1)
            #textitemboxi = boxi.boxi(screen, textitem, 100, 400, 0, BLUE, 2, BLACK, 0, 0)
            textitemboxi.register()
            # Column of savenames in boxis
            savesc = boxi.cboxiscroll(*cboxiscdef1, displayboxi1 = textitemboxi, displaykey1 = "imgname", displayfont = font20, displaycolor = BLACK )
            #savesc = boxi.cboxiscroll(screen,renderedtext,"render",300,400,1,WHITE,1,BLUE,0,0,7,displayboxi1 = textitemboxi, displaykey1 = "imgname", displayfont = font20, displaycolor = BLACK )
            
            #savesc = boxi.cboxiscroll(screen,renderedtext,"render",300,400,1,WHITE,1,BLUE,0,0,7,displayboxi1 = textitemboxi, displaykey1 = "wave", displayfont = font20, displaycolor = BLACK )
            savesc.register()
            # Pictures of a shell enemy
            shellsc = boxi.cboxi(screen, shells, "image", 40, 140, 1, BLACK, 1, RED,0,0)
            # Register for redraw events
            shellsc.register()
            # This row of boxis is not registered and will be covered by the timer based screen fill event.  
            # Other controls will be redrawn if they have called their register method.
            boxi.rboxi(screen, shells, "image", 600, 50, 1, BLACK, 1, RED,0,0)
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
                
                print("boxi!")
                boxi.boxi(screen,item,5, 15, 1, BLACK, 1, YELLOW, 0, 0)
            if event.key == K_DOWN:
                savesc.selectnext()
            
            if event.key == K_UP:
                savesc.selectprev()
    # Screen refresh at timer
    screen.fill((255, 255, 255))
    # Registered controls are redrawn
    boxi.drawregcontrols()
    clock.tick(30)

    # Flip the display
    pygame.display.flip()

# We're done, so we can quit now.
pygame.quit()
