# from matplotlib import animation
import imp
from matplotlib.pyplot import pause
import pygame
import os
import random
import csv
import SoundManager as sm
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
bg_tiling = 5
game_over = False
paused = False
option_one = False
option_two = False
option_three = False
variable = True
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
message_img = pygame.image.load('assets/img/background/paper-dialog.png').convert_alpha()
wellDone_img = pygame.image.load('assets/img/background/well-done-despicable-me.gif').convert_alpha()

#load images
pine1_img = pygame.image.load('Assets/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('Assets/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('Assets/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('Assets/Background/sky_cloud.png').convert_alpha()

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
#Creates the questions and answers for the games play. 
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
                answer2 = f'2. {g + h}'
                answer3 = f'3. {g}'
            numbersArray.append([f'{f}', f'What is {g*i} / {i}?', answer1, answer2, answer3])
    return numbersArray

test_array = createTestArray()

def draw_test(test_array):
    global test_index
    global variable
    test_message = test_array[test_index]

    text_renders = [font.render(test, True, (0, 120, 255)) for test in test_message]
    screen.blit(message_img, (0, 0))
    for i in range(len(text_renders)):
        if i != 0:
            screen.blit(text_renders[i], (SCREEN_WIDTH // 2 - text_renders[i].get_width() // 2, SCREEN_HEIGHT // 10 - text_renders[i].get_height() // 2 + i * text_renders[i].get_height()))
    # test 
    if option_one:
        if test_message[0] == '1':
            test_index  += 1
            #congratulation message
            print('congratulation')
            player.updateAction(3)
            sm.play_effect(0)
            variable = True
            return variable
        else:
            #wrong message
            if variable: 
                sm.play_effect(1)
            variable = False
            player.alive = False
            return variable 
    if option_two:
        if test_message[0] == '2':
            test_index += 1
            #congratulation message
            print('congratulation')
            player.updateAction(3)
            sm.play_effect(0)
            variable = True
            return variable
        else: 
            #wrong message
            if variable:
                sm.play_effect(1)
            variable = False
            player.alive = False  
            return variable
        
    if option_three:
        if test_message[0] == '3':
            test_index  += 1
        #congratulation message
            print('congratulation')
            player.updateAction(3)
            sm.play_effect(0)
            variable = True
            return variable
        else:
        #wrong message
            if variable:
                sm.play_effect(1)
            variable = False
            player.alive = False
            return variable 

# draw the game over screen
#create function for drawing background
def draw_bg():
	screen.fill(BG)
	width = sky_img.get_width()
	for x in range(bg_tiling):
		screen.blit(sky_img,      ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6,    SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img,    ((x * width) - bg_scroll * 0.7,    SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img,    ((x * width) - bg_scroll * 0.8,    SCREEN_HEIGHT - pine2_img.get_height()))

sm.play_theme(sm.theme_dungeon1_array)

# object containing data for the rendered tile map
class World():
    # arrays of each tile type
    def __init__(self):
        self.obstacle_list = []
        self.decoration_list = []
        self.water_list = []

    # maps each number in the tilemap with a tile png
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
                    # creates a dirt tile
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    # creates a water tile
                    elif tile >= 9 and tile <= 10:
                        self.water_list.append(tile_data)
                    # craetes a decoration tile
                    elif tile >= 11 and tile <= 14:
                        self.decoration_list.append(tile_data)
                    #create player
                    elif tile == 15:
                        player = Player("heroine",x * TILE_SIZE,y * TILE_SIZE,100,5)
                    #create ghost
                    elif tile == 16:
                        enemy = Ghost("Ghost",x * TILE_SIZE, y * TILE_SIZE,100,1)
                        enemy_group.add(enemy)
                    # creates monster/boss
                    elif tile == 20:
                        enemy = Ghost("Monster",x * TILE_SIZE, y * TILE_SIZE,120,1)
                        enemy_group.add(enemy)
        return player

    # renders each tile.png at the location indicated in the tilemap
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.decoration_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.water_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

    # updates the tiles rendered in the screen when the viewport/camera moves
    def update(self):
        self.rect.x += screen_scroll

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
        enemy.ai(player, TILE_SIZE, GRAVITY, world, screen_scroll)
        enemy.update()
        enemy.draw(screen)
    
        if player.rect.collidepoint(enemy.rect.center):
            enemy.speed = 0
            if player.speed != 0:
                sm.play_effect(2)
                old_Speed = player.speed 
            player.speed = 0
            player.jump = False
            if draw_test(test_array):
                enemy_group.remove(enemy)  
                player.speed = old_Speed          

                    
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
            if event.key == pygame.K_a and player.alive:# and not paused:
                moving_left = True
            if event.key == pygame.K_d and player.alive:# and not paused:
                moving_right = True
            if event.key == pygame.K_w and player.alive:# and not paused:
                moving_up = True
            if event.key == pygame.K_w and player.alive:# and not paused:
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

    if game_over:
            screen.blit(game_over_img, (SCREEN_WIDTH // 2 - game_over_img.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_img.get_height() // 2))

    sm.theme_queue(sm.theme_dungeon1_array)
    pygame.display.update()
#end while loop
    
pygame.quit()