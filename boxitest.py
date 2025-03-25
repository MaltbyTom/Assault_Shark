# Test surface for boxi.py

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
textitem = font20.render("A text object", 1, BLACK)

# Preload graphics
def get_image(key):
    if not key in image_cache:
        image_cache[key] = pygame.image.load("graphics/" + key).convert()
    return image_cache[key]


# Setup the window we'll use for drawing
screen = pygame.display.set_mode([800, 800])

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
savenamesc = {}
shellsc = {}
# returns number of saved games
listsize = edict.loadgame()
# Add rendered versions of savenames to dictionary
renderedtext = boxi.rendertext(edict.savedict, font20, RED)


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
            textitemboxi = boxi.boxi(screen, textitem, 100, 100, 0, BLUE, 2, BLACK, 0, 0)
            # Column of savenames in boxis
            savesc = boxi.cboxiscroll(screen,renderedtext,"render",300,400,1,WHITE,1,BLUE,0,0,3)
            for sel in savesc.cdict:
                # Select the first save game
                if savesc.cdict[sel]["boxi"].row == 0:
                    savesc.cdict[sel]["boxi"].selected = True 
                    # Draw the highlight
                    savesc.cdict[sel]["boxi"].draw(screen)
            # Initialize a column and row of boxis of shell pictures
            shellsc = boxi.cboxi(screen, shells, "image", 40, 140, 1, BLACK, 1, RED,0,0)
            boxi.rboxi(screen, shells, "image", 600, 50, 1, BLACK, 1, RED,0,0)
            # skip setup in future
            issetup = True

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == xbox360_controller.START:
                pause = False
                #pygame.mixer.music.play(loops=-1)
            if event.button == xbox360_controller.BACK:
                ingame = False
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                
                print("boxi!")
                boxi.boxi(screen,item,5, 15, 1, BLACK, 1, YELLOW, 0, 0)
            if event.key == K_DOWN:
                savesc.selectnext()
            
            if event.key == K_UP:
                savesc.selectprev()
    clock.tick(30)

    # Flip the display
    pygame.display.flip()

# We're done, so we can quit now.
pygame.quit()
