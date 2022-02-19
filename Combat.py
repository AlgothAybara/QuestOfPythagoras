from matplotlib import animation
import pygame
pygame.init


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Quest of Pythagoras")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define player action variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving_left_g = False
moving_right_g = False
moving_up_g = False
moving_down_g = True

#define colors
BG = (144,201,120)

def draw_bg():
    screen.fill(BG)
#close draw_bg function

class Ghost(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.frame_index = 0
        self.anim_index = 0
        self.FORCEUPDATE = False
        self.update_time = pygame.time.get_ticks()
        self.animation_types = ["idle"]
        self.animation_list = [[] for i in range(len(self.animation_types))]

        for i in range(len(self.animation_types)):
            for j in range(6):
                img = pygame.image.load(f'assets/sprites/{self.char_type}/{self.animation_types[i]}/{j}.png')
                img = pygame.transform.scale(img, (scale,scale))
                self.animation_list[i].append(img)
        self.image = self.animation_list[self.anim_index][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    #close __init__ constructor

    def move(self, moving_left, moving_right, moving_up, moving_down):
        # reset movement vars
        dx = 0
        dy = 0

        #assign movement variables if moving L or R
        if moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if moving_up:
            dy = -self.speed
            self.direction = -1
        if moving_down:
            dy = self.speed
            self.direction = 1
        if moving_left or moving_right or moving_up or moving_down:
            self.anim_index = 5
            

        #update rect position
        self.rect.x += dx
        self.rect.y += dy
    #close move function
        
    def updateAnimation(self):
        #update cooldown
        ANIMATION_COOLDOWN = 250
        self.image = self.animation_list[self.anim_index%1][self.frame_index%6]
        #check if time passed
        if pygame.time.get_ticks() -  self.update_time > ANIMATION_COOLDOWN or self.FORCEUPDATE:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            self.FORCEUPDATE = False
    #close updateAnimation function

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    #close draw function

#close Ghost class
class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.frame_index = 0
        self.anim_index = 0
        self.FORCEUPDATE = False
        self.update_time = pygame.time.get_ticks()
        self.animation_types = ["idle", "walk", "jump", "attack"]
        self.animation_list = [[] for i in range(len(self.animation_types))]

        for i in range(len(self.animation_types)):
            for j in range(2):
                img = pygame.image.load(f'assets/sprites/{self.char_type}/{self.animation_types[i]}/{j}.png')
                img = pygame.transform.scale(img, (scale,scale))
                self.animation_list[i].append(img)
        self.image = self.animation_list[self.anim_index][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    #close __init__ constructor

    def move(self, moving_left, moving_right, moving_up, moving_down):
        # reset movement vars
        dx = 0
        dy = 0

        #assign movement variables if moving L or R
        if moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if moving_up:
            dy = -self.speed
            self.direction = -1
            self.flip = True
        if moving_down:
            dy = self.speed
            self.direction = 1
            self.flip = False
        if moving_left or moving_right or moving_down or moving_up:
            self.anim_index = 1
            

        #update rect position
        self.rect.x += dx
        self.rect.y += dy
    #close move function
        
    def updateAnimation(self):
        #update cooldown
        ANIMATION_COOLDOWN = 250
        #updates image
        self.image = self.animation_list[self.anim_index][self.frame_index]

        #check if time passed
        if pygame.time.get_ticks() -  self.update_time > ANIMATION_COOLDOWN or self.FORCEUPDATE:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            self.FORCEUPDATE = False
        # reset index
        if (self.frame_index == len(self.animation_list[self.anim_index])):
            self.frame_index = 0
    #close updateAnimation function

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    #close draw function

#close player class

player = Player("heroine",200,200,100,5)

ghost = Ghost("ghost",500,500,100,1)
run = True
gMove = 0
while run:

    clock.tick(FPS)
    gMove += 1
    if gMove%60 == 0:
        if moving_down_g:
            moving_down_g = not moving_down_g
            moving_left_g = not moving_left_g
        elif moving_left_g:
            moving_up_g = not moving_up_g
            moving_left_g = not moving_left_g
        elif moving_up_g:
            moving_up_g = not moving_up_g
            moving_right_g = not moving_right_g
        elif moving_right_g:
            moving_right_g = not moving_right_g
            moving_down_g = not moving_down_g
        

    draw_bg()
    player.updateAnimation()
    ghost.updateAnimation()
    player.draw()
    ghost.draw()

    ghost.move(moving_left_g,moving_right_g,moving_up_g,moving_down_g)
    player.move(moving_left,moving_right,moving_up,moving_down)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False 
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
                ghost.FORCEUPDATE = True
            if event.key == pygame.K_d:
                moving_right = True
                ghost.FORCEUPDATE = True
            if event.key == pygame.K_w:
                moving_up = True
                ghost.FORCEUPDATE = True
            if event.key == pygame.K_s:
                moving_down = True
                ghost.FORCEUPDATE = True
            if event.key == pygame.K_ESCAPE:
                run == False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                ghost.anim_index = 0
            if event.key == pygame.K_d:
                moving_right = False
                ghost.anim_index = 0
            if event.key == pygame.K_w:
                moving_up = False
                ghost.anim_index = 0
            if event.key == pygame.K_s:
                moving_down = False
                ghost.anim_index = 0

        #Detect collisions for combat
        if player.rect.collidepoint(ghost.rect.center):
            run = False

    
    pygame.display.update()
#end while loop
    
    
    
    
pygame.quit()