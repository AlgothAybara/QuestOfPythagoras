# from matplotlib import animation
from matplotlib.pyplot import pause
import pygame
import os
import random
import csv
from characters.Ghost import Ghost
from characters.Player import Player

pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Quest of Pythagoras")

#set framerate
clock = pygame.time.Clock()
FPS = 60
#define game variables
SCROLL_THRESH = 200
GRAVITY = 0.3
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1
screen_scroll = 0
bg_scroll = 0
game_over = False
paused = False
option_one = False
option_two = False
option_three = False

#define player action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
#define ghost action variables
moving_left_g = False
moving_right_g = False
moving_up_g = False
moving_down_g = True

#load images for background
game_over_img = pygame.image.load('assets/img/background/32847539f3d1e018a00145a3848f67e8.jpeg').convert_alpha()
mountain_img = pygame.image.load('assets/img/background/Valley-Taurus-Mountains-Turkey.jpeg').convert_alpha()
message_img = pygame.image.load('assets/img/background/paper-dialog.png').convert_alpha()
wellDone_img = pygame.image.load('assets/img/background/well-done-despicable-me.gif').convert_alpha()

# load sounds
#attack_sound = pygame.mixer.Sound("assets/audio/EFFECT_Attack.wav")
#missed_sound = pygame.mixer.Sound("assets/audio/EFFECT_Missed.wav")

# set sound levels
#attack_sound.set_volume(0.5)
#missed_sound.set_volume(0.5)

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Assets/img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#define colors
BG = (144,201,120)

#promp iteraction with player
test = False
test_index = 0
font = pygame.font.SysFont('Times New Roman', 50)
def createTestArray():
    numbersArray = []
    for x in range(20):
        f = random.randint(1,3)
        g = random.randint(1,12)
        h = random.randint(1,12)
        i = random.randint(2,3)
        if x < 2:
            if f == 1:
                answer1 = f'1. {g + h}'
                answer2 = f'2. {g - h}'
                answer3 = f'3. {h * g}'
            elif f == 2: 
                answer1 = f'1. {g - h}'
                answer2 = f'2. {g + h}'
                answer3 = f'3. {h * g}'
            elif f == 3: 
                answer1 = f'1. {g - h}'
                answer2 = f'2. {g * h}'
                answer3 = f'3. {h + g}'
            numbersArray.append([f'{f}', f'What is {g} + {h}?', answer1, answer2, answer3])
        elif x < 4:
            if f == 1:
                answer1 = f'1. {g - h}'
                answer2 = f'2. {g + h}'
                answer3 = f'3. {h * g}'
            elif f == 2: 
                answer1 = f'1. {g + h}'
                answer2 = f'2. {g - h}'
                answer3 = f'3. {h * g}'
            elif f == 3: 
                answer1 = f'1. {g + h}'
                answer2 = f'2. {g * h}'
                answer3 = f'3. {g - h}'
            numbersArray.append([f'{f}', f'What is {g} - {h}?', answer1, answer2, answer3])
        elif x < 6:
            if f == 1:
                answer1 = f'1. {g * h}'
                answer2 = f'2. {g * (h+1)}'
                answer3 = f'3. {h * (g+1)}'
            elif f == 2: 
                answer1 = f'1. {g * (h+1)}'
                answer2 = f'2. {g * h}'
                answer3 = f'3. {h * (g+1)}'
            elif f == 3: 
                answer1 = f'1. {(g+1) * h}'
                answer2 = f'2. {g * (h+1)}'
                answer3 = f'3. {h * g}'
            numbersArray.append([f'{f}', f'What is {g} x {h}?', answer1, answer2, answer3])
        elif x < 20:
            if f == 1:
                answer1 = f'1. {g}'
                answer2 = f'2. {g + i}'
                answer3 = f'3. {g*i -i}'
            elif f == 2: 
                answer1 = f'1. {g - h}'
                answer2 = f'2. {g}'
                answer3 = f'3. {h * g}'
            elif f == 3: 
                answer1 = f'1. {g - h}'
                answer2 = f'2. {g * h}'
                answer3 = f'3. {g}'
            numbersArray.append([f'{f}', f'What is {g*i} / {i}?', answer1, answer2, answer3])
    return numbersArray

test_array = createTestArray()

def toggle_pause_and_test():
    global paused
    global test
    paused = not paused
    test = not test


def draw_test(test_array):
    global test_index
    variable = False
    test_message = test_array[test_index]

    text_renders = [font.render(test, True, (0, 120, 255)) for test in test_message]
    screen.blit(message_img, (0, 0))
    for i in range(len(text_renders)):
        if i != 0:
            screen.blit(text_renders[i], (SCREEN_WIDTH // 2 - text_renders[i].get_width() // 2, SCREEN_HEIGHT // 10 - text_renders[i].get_height() // 2 + i * text_renders[i].get_height()))
    # test 
    if option_one:
        toggle_pause_and_test()
        if test_message[0] == '1':
            test_index  += 1
            #congratulation message
            print('congratulation')
            player.updateAction(3)
            #pygame.mixer.Sound.play(attack_sound)
            variable = True
            return variable
        else:
            #wrong message
            print('wrong')
            variable = False
            player.alive = False
            #pygame.mixer.Sound.play(missed_sound)
            return variable 
    if option_two:
        toggle_pause_and_test()
        if test_message[0] == '2':
            test_index  += 1
            #congratulation message
            print('congratulation')
            player.updateAction(3)
            #pygame.mixer.Sound.play(attack_sound)
            variable = True
            return variable
        else: 
            #wrong message
            variable = False
            player.alive = False
            #pygame.mixer.Sound.play(missed_sound)
            return variable
        
    if option_three:
        toggle_pause_and_test()
        if test_message[0] == '3':
            test_index  += 1
        #congratulation message
            print('congratulation')
            player.updateAction(3)
            #pygame.mixer.Sound.play(attack_sound)
            variable = True
            return variable
        else:
        #wrong message
            print('wrong')
            variable = False
            player.alive = False
            #pygame.mixer.Sound.play(missed_sound)
            return variable 
    


# draw the game over screen
def draw_bg():
    screen.fill(BG)
    width = mountain_img.get_width()
    for x in range(5):
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 0))
        #close draw_bg function

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:#create player
                        player = Player("heroine",x * TILE_SIZE,y * TILE_SIZE,100,5)
                    elif tile == 16:#create enemies

                        enemy = Ghost("ghost",x * TILE_SIZE, y * TILE_SIZE,100,1)
                        # enemy = Ghost('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)


        return player


    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
    def update(self):
        self.rect.x += screen_scroll
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


#create sprite groups
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
decoration_group.draw(screen)



#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world
with open(f'Assets/Archived/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player = world.process_data(world_data)



run = True
while run:
    #if player is dead, end game
    if not player.alive:
        game_over = True
    clock.tick(FPS)
    
    #draw background
    draw_bg()
    #draw world map
    world.draw()

    #update and draw groups
    item_box_group.update()
    decoration_group.update()
    water_group.update()
    for enemy in enemy_group:
        enemy.ai(player, TILE_SIZE, GRAVITY, world, screen_scroll, paused, toggle_pause_and_test)
        enemy.update()
        enemy.draw(screen)
        if player.rect.collidepoint(enemy.rect.center):
                if draw_test(test_array):
                    enemy_group.remove(enemy)  
                    toggle_pause_and_test()


           

                    
    player.updateAnimation()
    player.draw(screen)

    player.move(moving_left,moving_right, GRAVITY, world, SCREEN_WIDTH, SCROLL_THRESH, bg_scroll, TILE_SIZE, SCREEN_HEIGHT)
    if player.alive:
        #player attacking
        #throw grenades
        if player.in_air:
            player.updateAction(2)#2: jump
        elif moving_left or moving_right:
            player.updateAction(1)#1: run
        elif player.attack:
            player.updateAction(3)#3: fight
        else:
            player.updateAction(0)#0: idle

        player.move(moving_left, moving_right, GRAVITY, world, SCREEN_WIDTH, SCROLL_THRESH, bg_scroll, TILE_SIZE, SCREEN_HEIGHT)
        screen_scroll = player.move(moving_left, moving_right, GRAVITY, world, SCREEN_WIDTH, SCROLL_THRESH, bg_scroll, TILE_SIZE, SCREEN_HEIGHT)
        bg_scroll -= screen_scroll

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False 
        #keyboard presses
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                option_one = True
            if event.key == pygame.K_2:
                option_two = True
            if event.key == pygame.K_3:
                option_three = True
            if event.key == pygame.K_a and not paused:
                moving_left = True
            if event.key == pygame.K_d and not paused:
                moving_right = True
            if event.key == pygame.K_w and not paused:
                moving_up = True
            if event.key == pygame.K_w and player.alive and not paused:
                player.jump = True
            if event.key == pygame.K_SPACE:
                player.attack = True
            if event.key == pygame.K_ESCAPE:
                run == False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                option_one = False
            if event.key == pygame.K_2:
                option_two = False
            if event.key == pygame.K_3:
                option_three = False
            if event.key == pygame.K_a:
                moving_left = False
                player.anim_index = 0
            if event.key == pygame.K_d:
                moving_right = False
                player.anim_index = 0
            if event.key == pygame.K_w:
                moving_up = False
                player.anim_index = 0
            if event.key == pygame.K_s:
                moving_down = False
                player.anim_index = 0
            if event.key == pygame.K_SPACE:
                player.attack = False
                player.anim_index = 0 
        #Detect collisions for combat
        # if player.rect.collidepoint(ghost.rect.center):
        #     run = False
    # interaction with items
    #if test:
        #draw_test(test_array)
    if game_over:
            screen.blit(game_over_img, (SCREEN_WIDTH // 2 - game_over_img.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_img.get_height() // 2))

    pygame.display.update()
#end while loop
    
pygame.quit()