import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x
        self.y_pos = y
        self.scale = scale

        img = pygame.image.load('assets/sprites/heroine/heroine_still.png')
        self.image = pygame.transform.scale(img, (scale,scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)
