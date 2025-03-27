# Enemy Dictionary Library - Assault Shark project
# Written by Tom Maltby, [c]Tom Maltby 2025, credits follow
# www.maltby.org

import pygame
import tkinter
import json
import os
import glob

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
SCREEN_WIDTH = root.winfo_screenwidth() # - 50
SCREEN_HEIGHT = root.winfo_screenheight() # - 100
SCREEN_HEIGHT_NOBOX = SCREEN_HEIGHT - 100   

def loadgame():
    added = 0
    # Gets a list of all jsons in the JSON directory
    jsons = glob.glob ("json/savepoint/*.json")
    # Loads all jsons into the savedict dictionary
    
    for jsonf in jsons:
        json_name = os.path.basename(jsonf)
        # only input the savepoint into savedict
        if json_name.startswith("savepoint"):
            with open("json/savepoint/" + json_name, "r") as jsonfile:
                addtodict = json.load(jsonfile)
                savedict.update(addtodict)
                #print(json_name)
                #print(addtodict)
                added += 1
    #print("savedict")
    #print(savedict)
    return added

def addjsons():
    added = 0
    # Gets a list of all jsons in the JSON directory
    jsons = glob.glob ("json/*.json")
    # Loads all jsons into the enemydict dictionary
    for jsonf in jsons:
        json_name = os.path.basename(jsonf)
        # don't input the template into enemydict
        if json_name != "fullblank.json":
            with open("json/" + json_name, "r") as jsonfile:
                addtodict = json.load(jsonfile)
                enemydict.update(addtodict)
                added += 1
    return added

#def gencompleteblank():
    #blankrecord = {}
    #for etype, etypeval in enemydict.items():
        #for prop, propval in etypeval.items():
            #if prop in blankrecord:
                #if blankrecord.get(prop):
                    #noupdate = True
                #else:
                    #if type(propval) == Color:
                    #if propval == WHITE:
                        #propval = "#FFFFFF"
                    #blankrecord[prop] = propval
            #else:
                #blankrecord[prop] = propval
    #print(blankrecord)
    #print(str(len(blankrecord)) + "properties gathered")
    #with open("JSON/fullblank.json", "w") as file:
        #json.dump(blankrecord, file, indent=4)
    #return len(blankrecord)

savedict = {
}  

# Fill a nested dictionary of enemies by etype
enemydict = {
    "e_spawn_umiss1": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":25,
        # Missile, unguided
        "imgname": "missile1.png",
        "mask": "#FFFFFF",
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [5,20],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [-1,1],
        # Limits for climb/dive
        "climbmax": 8,
        "climbmin": -8,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [0,1],
        "centerheight": [0,1],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 15,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": [10,5,0],    
        # Animation frame names   
        "aniframes": ["missile1.png","missile1b.png","missile1c.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_62",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage to player if collided
        "damage": [10,20],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_spawn_hsnek2": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Homing Snek
        "imgname": "snek1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 15, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": True,
        "climb": [0,1],
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": -3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -30,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 10,
        # Number of animation frames
        "numaniframes": 2,
        # Timing for animation frames
        "aniframetimers": [5,0],    
        # Animation frame names   
        "aniframes": ["snek1.png","snek2.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_62",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [15,30],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_spawn_hmiss3": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Homing Missile
        "imgname": "missile21.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 16, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": True,
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 9,
        "climbmin": -9,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher object, 
        # otherwise they may be tuples to generate starting position with randint
        "islauncher": True,
        "centerwidth": -20,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 8,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": [5,3,0],    
        # Animation frame names   
        "aniframes": ["missile21.png","missile22.png","missile23.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_62",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [15,30],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_spawn_blimp4": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":5,
        # Blue blimp, unarmored
        "imgname": "ship4.png",
        "mask": BLACK, # Blimps are leftover from the VB They Comin, and have black for a mask color
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [5,10],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [-1,1],
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": -3,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": "e_spawn_hsnek2",
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [0,1],
        "centerheight": [0,1],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,             
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_61",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 20,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 4,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [30,45],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_spawn_blimpa5": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":5,
        # Red blimp, armored
        "imgname": "ship4a.png",
        "mask": BLACK, # Blimps are leftover from the VB They Comin, and have black for a mask color
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [5,10],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [-1,1],
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": -3,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": "e_spawn_hfish6",
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [0,1],
        "centerheight": [0,1],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_61",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 20,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 5,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [40,60],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_spawn_hfish6": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Homing Fish
        "imgname": "fish1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 20, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": True,
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": -4,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -38,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 2,
        # Timing for animation frames
        "aniframetimers": [6,0],    
        # Animation frame names   
        "aniframes": ["fish1.png","fish1a.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_62",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [20,35],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_g_cannon7": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Cannon
        "imgname": "gun1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": "e_ammo_shell81",
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": +60,
        "centerheight": -20,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,         
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_64",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 25,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 2,
        "ispowerup": False,
        "isgun": True,
        # Tuple for range of damage
        "damage": [25,40],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_g_misslaunch8": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":5,
        # Missile Launcher
        "imgname": "gun2.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": "e_spawn_hmiss3",
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": True,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": SCREEN_WIDTH + 30,
        "centerheight": SCREEN_HEIGHT_NOBOX -33,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_63",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 35,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 2,
        "ispowerup": False,
        "isgun": True,
        # Tuple for range of damage
        "damage": [25,40],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_boss_cutboss41": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Cuttleboss 1
        "imgname": "shell3.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": True,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": [1,3],
        # Limits for climb/dive
        "climbmax": 5,
        "climbmin": -5,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": True,
        # Ammo type if isshooter
        "ammotype": ["e_spawn_hsnek2","e_spawn_hmiss3","e_spawn_hfish6"],
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": SCREEN_WIDTH + 30,
        "centerheight": SCREEN_HEIGHT_NOBOX / 2,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": [8,4,0],    
        # Animation frame names   
        "aniframes": ["shell3.png","shell3b.png", "shell3c.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_65",
        # Missiles and shells have one hp; blimps and guns have more, bosses have many
        "hp": 1000,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [50,100],
        # is boss?
        "boss": 1,
        # boomcounter for explosion timing
        "boomcounter": 35,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_exp_61": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Exploded blimp
        "imgname": "ship4xp1.png",
        "mask": BLACK,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 3,
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": 3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": [8,5,0],
        # expframes is a tuple of explosion frames
        "expframes": ["ship4xp1.png","ship4xp2.png","ship4xp3.png"],
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [15,40],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_exp_62": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Exploded missile or cannon shell
        "imgname": "boom1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 3,
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": 3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": [8,5,0],
        # expframes is a tuple of explosion frames
        "expframes": ["boom.png","boom2.png","boom3.png"],
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [5,10],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 12,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_exp_63": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Exploded Missile Launcher
        "imgname": "gun2xp1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": True,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": [8,5,0],
        # expframes is a tuple of explosion frames
        "expframes": ["gun2xp1.png","gun2xp2.png","gun2xp3.png"],
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [5,40],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_exp_64": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Exploded Cannon
        "imgname": "gun1xp1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 5, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": 0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": True,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 3,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": [8,5,0],
        # expframes is a tuple of explosion frames
        "expframes": ["gun1xp1.png","gun1xp2.png","gun1xp3.png"],
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [5,40],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_exp_65": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Exploded boss
        "imgname": "shell3xp1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 10, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 3,
        # Limits for climb/dive
        "climbmax": 3,
        "climbmin": 3,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": 0,
        "centerheight": 0,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": True,
        "numexpframes": 4,
        # expframetimers are a countdown of ticks in each frame
        "expframetimers": [18,12,6,0],
        # expframes is a tuple of explosion frames
        "expframes": ["shell3xp1.png","shell3xp2.png","shell3xp3.png","shell3xp4.png"],
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [15,40],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_ammo_shell81": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Cannon Shell
        "imgname": "bullete1.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 15, 
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": -5,
        # Limits for climb/dive
        "climbmax": 2,
        "climbmin": -5,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": True,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": True,
        "centerwidth": -5,
        "centerheight": -5,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,      
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": "e_exp_62",
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [15,25],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 100,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_tent_tentacle91": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight":0,
        # Boss tentacle attack
        "imgname": "tentacle7.png",
        "mask": WHITE,
        # Advanced movement flag
        "advancedmovement": True,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": False,
        "speed": 0, 
        # If climb is random, climb passes a tuple, otherwise a single value
        "randclimb": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "ishoming": False,
        "climb": 0,
        # Limits for climb/dive
        "climbmax": 0,
        "climbmin": -0,
        # Is location random
        "randcenter": False,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher object, 
        # otherwise they may be tuples to generate starting position with randint
        "islauncher": True,
        "centerwidth": 20,
        "centerheight": 100,
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 34,
        # Number of animation frames
        "numaniframes": 17,
        # Timing for animation frames
        "aniframetimers": [32,30,28,26,24,22,20,18,16,14,12,10,8,6,4,2,0],    
        # Animation frame names   
        "aniframes": ["tentacle7.png","tentacle6.png","tentacle5.png","tentacle4.png","tentacle4.png","tentacle3.png","tentacle2.png","tentacle.png",
                      "tentacleup.png","tentacle.png","tentacledown.png","tentacle.png","tentacle2.png","tentacle3.png","tentacle4.png","tentacle5.png",
                      "tentacle6.png","tentacle7.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": False,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 300,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": False,
        # Tuple for range of damage
        "damage": [25,75],
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 0,
        # perc damage from enemies
        "damenemies": 0,
        # perc damage from bullets
        "dambullets": 100,
        # perc damage from player collision
        "damplayer": 100,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_life111": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Life Powerup
        "imgname": "extralife.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": [6,3,0],    
        # Animation frame names   
        "aniframes": ["extralife.png","extralife2.png","extralife3.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_flamer112": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Flamer Powerup
        "imgname": "powerupflamer.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_shock113": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Shock Powerup
        "imgname": "powerupshock.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_bio114": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Bio Blaster Powerup
        "imgname": "powerupbio.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_pulsar115": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Pulsar Powerup
        "imgname": "poweruppulse.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_health116": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Health Powerup
        "imgname": "poweruphealth.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_armor117": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 3,
        # Armor Powerup
        "imgname": "poweruparmor.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": False,
        "ticks": 0,       
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_healthmax118": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 2,
        # Healthmax Powerup
        "imgname": "poweruphealthmax.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": [6,3,0],    
        # Animation frame names   
        "aniframes": ["poweruphealthmax.png","poweruphealthmax1.png","poweruphealthmax2.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_armormax119": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 2,
        # Armormax Powerup
        "imgname": "poweruparmormax.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 12,
        # Number of animation frames
        "numaniframes": 3,
        # Timing for animation frames
        "aniframetimers": [6,3,0],    
        # Animation frame names   
        "aniframes": ["poweruparmormax.png","poweruparmormax1.png","poweruparmormax2.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgmulti2": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 2,
        # MG Powerup Multishot 2
        "imgname": "powerupmgx2.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgx2.png","powerupmgx2b.png","powerupmgx2c.png","powerupmgx2d.png","powerupmgx2e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgmulti3": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 2,
        "spawnweight": 2,
        # MG Powerup Multishot 3
        "imgname": "powerupmgx3.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgx3.png","powerupmgx3b.png","powerupmgx3c.png","powerupmgx3d.png","powerupmgx3e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgmulti5": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 4,
        "spawnweight": 2,
        # MG Powerup Multishot 5
        "imgname": "powerupmgx5.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgx5.png","powerupmgx5b.png","powerupmgx5c.png","powerupmgx5d.png","powerupmgx5e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgmulti7": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 6,
        "spawnweight": 2,
        # MG Powerup Multishot 7
        "imgname": "powerupmgx7.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgx7.png","powerupmgx7b.png","powerupmgx7c.png","powerupmgx7d.png","powerupmgx7e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgammo_laser2": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 2,
        # MG Powerup Laser Ammo
        "imgname": "powerupmga2.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmga2.png","powerupmga2b.png","powerupmga2c.png","powerupmga2d.png","powerupmga2e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgammo_plasma3": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 4,
        "spawnweight": 2,
        # MG Powerup Plasma Ammo
        "imgname": "powerupmga3.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmga3.png","powerupmga3b.png","powerupmga3c.png","powerupmga3d.png","powerupmga3e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgb1": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 1,
        "spawnweight": 2,
        # MG Powerup Bounce
        "imgname": "powerupmgb1.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgb1.png","powerupmgb1b.png","powerupmgb1c.png","powerupmgb1d.png","powerupmgb1e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgb2": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 2,
        "spawnweight": 2,
        # MG Powerup Bounce 2
        "imgname": "powerupmgb2.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgb2.png","powerupmgb2b.png","powerupmgb2c.png","powerupmgb2d.png","powerupmgb2e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    },
    "e_pu_mgb3": {
        # First level spawned on, and weight of possible spawns
        "firstspawn": 5,
        "spawnweight": 2,
        # MG Powerup Bounce 3
        "imgname": "powerupmgb3.png",
        "mask": WHITE, 
        # Advanced movement flag
        "advancedmovement": False,
        # If speed is random, speed passes a tuple, otherwise a single value
        "randspeed": True,
        "speed": [-1,1],
        # If climb is random, speed passes a tuple, otherwise a single value
        "randclimb": True,
        "ishoming": False,
        # If homing armament, climb must be a tuple for randint, and is +/- modified by player's position relative to enemy position
        "climb": [1,2],
        # Limits for climb/dive
        "climbmax": 4,
        "climbmin": 1,
        # Is location random
        "randcenter": True,
        # Does the enemy shoot
        "isshooter": False,
        # Ammo type if isshooter
        "ammotype": 0,
        # Does it explode at peak height
        "skyburst": False,
        # Is enemy intended on ground
        "isground": False,
        # If islauncher, then centerwidth and centerheight are single values to modify top and left of launcher, otherwise they are tuples
        # to generate starting position with randint
        "islauncher": False,
        "centerwidth": [100, SCREEN_WIDTH -100],
        "centerheight": [-10, 0],
        # If isanimated, the non-exploding version of the armament animates itself from ticks; explosion animations are handled with boomcounter
        "isanimated": True,
        # Total ticks to recycle animation timer at
        "ticks": 20,
        # Number of animation frames
        "numaniframes": 5,
        # Timing for animation frames
        "aniframetimers": [16,12,8,4,0],    
        # Animation frame names   
        "aniframes": ["powerupmgb3.png","powerupmgb3b.png","powerupmgb3c.png","powerupmgb3d.png","powerupmgb3e.png"],
        # If isexploded, animates once through on boomcounter, then dies
        "isexploded": False,
        # If isexplodable, eplodes before dying into etype isexplodable
        "isexplodable": 0,
        # Missiles and shells have one hp; blimps and guns have more
        "hp": 1,
        # Fired is a flag acting as a single frame timer to give missiles time to get clear of the launcher
        "fired": 0,
        "ispowerup": True,
        # is boss?
        "boss": 0,
        # boomcounter for explosion timing
        "boomcounter": 20,
        # perc damage from ground
        "damground": 0,
        # perc damage from mountain
        "dammountain": 100,
        # perc damage from enemies
        "damenemies": 100,
        # perc damage from bullets
        "dambullets": 0,
        # perc damage from player collision
        "damplayer": 0,
        "multishot": 0,
        "burstminmax": [0,1],
        "islayer": 0,
        "eggtype": "e_spawn_hsnek2",
        "multilay": 0,
        "clutchminmax": [0,1]
    }
}
