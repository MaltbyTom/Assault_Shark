# Some original sounds sourced  Jon Fincher
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
#
# Additional sounds from -- http://rpg.hamsterrepublic.com/ohrrpgce/Free_Sound_Effects#Battle_Sounds
# mg2loop sound from Machine Gun 002 - loop.ogg by pgi -- https://freesound.org/s/212608/ -- License: Creative Commons 0
# laser sound from Laser2 by Daleonfire -- https://freesound.org/s/505235/ -- License: Creative Commons 0
# Boss laugh from Laugh 1.wav by Ballistiq85 -- https://freesound.org/s/211566/ -- License: Attribution 3.0, Reverb added with Audacity
# Ride of the Valkyries 8 bit from -- https://archive.org/details/RichardWagnerRideOfTheValkyries8BitsVersion https://creativecommons.org/licenses/by-sa/3.0/
# Tentacle sound trimmed from -- Pumpmkin Guts Squish 1.aif by MWLANDI -- https://freesound.org/s/85862/ -- License: Attribution 3.0
# Level reward drop sound from -- Powerup 08.wav by LilMati -- https://freesound.org/s/523648/ -- License: Creative Commons 0
# Warp sound trimmed from -- warping by oganesson -- https://freesound.org/s/555017/ -- License: Creative Commons 0
# Game over sound from -- Game Over 08.wav by LilMati -- https://freesound.org/s/524741/ -- License: Creative Commons 0
# Die sound from -- Monster-Die.ogg by deleted_user_4798915 -- https://freesound.org/s/276443/ -- License: Attribution 3.0

import pygame

backmusic = None

def setupsounds():
    sounds = {}
    pygame.mixer.set_reserved(2)
    # Load and play our background music
    #pygame.mixer.music.load("sounds/apoxode_-_electric_1.mp3")
    pygame.mixer.music.load("sounds/ride8bit.ogg")
    #sounds["music"] = pygame.mixer_music

    # Load all our sound files
    move_up_sound = pygame.mixer.Sound("sounds/rising_putter.ogg")
    sounds["move_up_sound"] = move_up_sound
    move_down_sound = pygame.mixer.Sound("sounds/falling_putter.ogg")
    sounds["move_down_sound"] = move_down_sound
    shoot_sound = pygame.mixer.Sound("sounds/shoot.ogg")
    sounds["shoot_sound"] = shoot_sound
    laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
    sounds["laser_sound"] = laser_sound
    shoot2_sound = pygame.mixer.Sound("sounds/mg2loop.ogg")
    sounds["shoot2_sound"] = shoot2_sound
    collision_sound = pygame.mixer.Sound("sounds/small_explosion.ogg")
    sounds["collision_sound"] = collision_sound
    bio_sound = pygame.mixer.Sound("sounds/bio_splat.ogg")
    sounds["bio_sound"] = bio_sound
    shock_sound = pygame.mixer.Sound("sounds/shock_sound2.ogg")
    sounds["shock_sound"] = shock_sound
    flamer_sound = pygame.mixer.Sound("sounds/flamer_sound.ogg")
    sounds["flamer_sound"] = flamer_sound
    powerup_sound = pygame.mixer.Sound("sounds/power_up.ogg")
    sounds["powerup_sound"] = powerup_sound
    wavechange_sound = pygame.mixer.Sound("sounds/wave_change.ogg")
    sounds["wavechange_sound"] = wavechange_sound
    pulse_sound = pygame.mixer.Sound("sounds/pulse_sound.ogg")
    sounds["pulse_sound"] = pulse_sound
    boss_sound = pygame.mixer.Sound("sounds/bosslaugh.ogg")
    sounds["boss_sound"] = boss_sound
    tentacle_sound = pygame.mixer.Sound("sounds/tentacle.ogg")
    sounds["tentacle_sound"] = tentacle_sound    
    reward_sound = pygame.mixer.Sound("sounds/reward.ogg")
    sounds["reward_sound"] = reward_sound  
    warp_sound = pygame.mixer.Sound("sounds/warp.ogg")
    sounds["warp_sound"] = warp_sound
    die_sound = pygame.mixer.Sound("sounds/die.ogg")
    sounds["die_sound"] = die_sound 
    gameover_sound = pygame.mixer.Sound("sounds/gameover.ogg")
    sounds["gameover_sound"] = gameover_sound


    # Set the base volume for all sounds
    move_up_sound.set_volume(0.5)
    move_down_sound.set_volume(0.5)
    collision_sound.set_volume(0.5)
    shoot_sound.set_volume(0.5)
    laser_sound.set_volume(0.5)
    shoot2_sound.set_volume(0.5)
    bio_sound.set_volume(0.5)
    shock_sound.set_volume(0.5)
    flamer_sound.set_volume(0.5)
    powerup_sound.set_volume(0.5)
    wavechange_sound.set_volume(0.5)
    pulse_sound.set_volume(0.5)
    boss_sound.set_volume(1)
    tentacle_sound.set_volume(.5)
    reward_sound.set_volume(1)
    warp_sound.set_volume(1)
    die_sound.set_volume(1)
    gameover_sound.set_volume(1)

    return(sounds)

def stopsounds(sounds):
    for sound in sounds:
        sounds[sound].stop()