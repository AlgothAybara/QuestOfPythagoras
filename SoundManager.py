import pygame
import random

pygame.init()
pygame.mixer.init()

SONG_END = pygame.USEREVENT + 1

# load sound effects
attack_effect = pygame.mixer.Sound("assets/audio/effects/attack.wav")
missed_effect = pygame.mixer.Sound("assets/audio/effects/missed.wav")
encounter_effect = pygame.mixer.Sound("assets/audio/effects/encounter.wav")

effect_array = [attack_effect, missed_effect, encounter_effect]

# set sound levels
for effect in effect_array:
    effect.set_volume(0.3)

# load Dungeon1 theme
dungeon1_intro = "assets/audio/dungeon1/intro.wav"
dungeon1_bridge = "assets/audio/dungeon1/bridge.wav"
dungeon1_filler = "assets/audio/dungeon1/filler.wav"
dungeon1_solo = "assets/audio/dungeon1/solo.wav"
dungeon1_verse1 = "assets/audio/dungeon1/verse1.wav"
dungeon1_verse2 = "assets/audio/dungeon1/verse2.wav"
dungeon1_verse3 = "assets/audio/dungeon1/verse3.wav"
dungeon1_silence = "assets/audio/dungeon1/silence.wav"


theme_dungeon1_array = [
    dungeon1_intro,
    dungeon1_bridge,
    dungeon1_filler,
    dungeon1_solo,
    dungeon1_verse1,
    dungeon1_verse2,
    dungeon1_verse3,
    dungeon1_silence,
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

def play_theme(theme):
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load(theme[0])
    pygame.mixer.music.queue(theme[1])
    pygame.mixer.music.play()

    
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

def theme_queue(theme):
    index = random.randint(0,len(theme)-1)
    pygame.mixer.music.queue(theme[index])
    # for event in pygame.event.get():
    #     if event.type == SONG_END:
    #         print("Na dog")
    #         index = random.randint(0,len(theme)-1)
    #         pygame.mixer.music.queue(theme[index])


    



