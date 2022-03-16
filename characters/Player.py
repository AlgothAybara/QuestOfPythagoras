import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.jump = False
        self.attack = False
        self.in_air = True
        self.vel_y = 0
        self.frame_index = 0
        self.anim_index = 0
        self.action = 0
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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    #close __init__ constructor

    def move(self, moving_left, moving_right, GRAVITY, world, SCREEN_WIDTH, SCROLL_THRESH, bg_scroll, TILE_SIZE, SCREEN_HEIGHT):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

         #check if going off the edges of the screen
        if self.char_type == 'heroine':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        #update scroll based on player position
        if self.char_type == 'heroine':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.alive = False

        return screen_scroll
    #close move function
        
    def updateAnimation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
    #close updateAnimation function
    def updateAction(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    #close draw function
