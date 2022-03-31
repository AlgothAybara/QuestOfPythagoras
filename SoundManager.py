import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

# load sound effects
attack_effect = pygame.mixer.Sound("assets/audio/effects/attack.wav")
missed_effect = pygame.mixer.Sound("assets/audio/effects/missed.wav")
encounter_effect = pygame.mixer.Sound("assets/audio/effects/encounter.wav")

effect_array = [attack_effect, missed_effect, encounter_effect]

# set sound levels
for effect in effect_array:
    effect.set_volume(0.4)

# load Dungeon1 theme
dungeon1_intro = "assets/audio/dungeon1/intro.wav"
dungeon1_bridge = "assets/audio/dungeon1/bridge.wav"
dungeon1_filler = "assets/audio/dungeon1/filler.wav"
dungeon1_solo = "assets/audio/dungeon1/solo.wav"
dungeon1_verse1 = "assets/audio/dungeon1/verse1.wav"
dungeon1_verse2 = "assets/audio/dungeon1/verse2.wav"
dungeon1_verse3 = "assets/audio/dungeon1/verse3.wav"

# creates a dungeon theme array
theme_dungeon1_array = [
    dungeon1_intro,
    dungeon1_bridge,
    dungeon1_filler,
    dungeon1_solo,
    dungeon1_verse1,
    dungeon1_verse2,
    dungeon1_verse3,
]

# plays sound effect in the effect array
def play_effect(num):
    '''
    Plays sound effect in the effect_array.
    0 - attack;
    1 - missed;
    2 - encounter;
    '''
    pygame.mixer.Sound.play(effect_array[num])
    #end play_effect function

# plays the mixer.music object
def play_theme(theme):
    pygame.mixer.music.load(theme[0])
    pygame.mixer.music.queue(theme[1])
    pygame.mixer.music.play()

# appneds random clip to the array
def theme_queue(theme):
    index = random.randint(0,len(theme)-2)    
    pygame.mixer.music.queue(theme[index])