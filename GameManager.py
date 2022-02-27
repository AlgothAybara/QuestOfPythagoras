# from matplotlib import animation
import pygame
import os
import csv
from characters.Ghost import Ghost
from characters.Player import Player
pygame.init


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
mountain_img = pygame.image.load('assets/img/background/Valley-Taurus-Mountains-Turkey.jpeg').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Assets/img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#define colors
BG = (144,201,120)

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
        run = False
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
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run == False

        #keyboard button released
        if event.type == pygame.KEYUP:
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
        #Detect collisions for combat
        # if player.rect.collidepoint(ghost.rect.center):
        #     run = False
    
    pygame.display.update()
#end while loop
    
pygame.quit()