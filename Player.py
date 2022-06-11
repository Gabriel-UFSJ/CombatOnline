import pygame

class Player():
    def __init__(self,X,Y,WIDTH,HEIGHT,OBJECT):
        self.x = X
        self.y = Y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.OBJECT = OBJECT
        self.rect = (X,Y,WIDTH,HEIGHT)
        self.VEL = 3

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.OBJECT, self.rect)

    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]: # LEFT
            self.x -= self.VEL
        if keys_pressed[pygame.K_d]: # RIGHT
            self.x += self.VEL
        if keys_pressed[pygame.K_w]: # UP
            self.y -= self.VEL
        if keys_pressed[pygame.K_s]: # DOWN
            self.y += self.VEL
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.WIDTH, self.HEIGHT)
