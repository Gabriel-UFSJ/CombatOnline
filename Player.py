from operator import truediv
from re import purge
import pygame
import os

##hulls##
TANK_WIDTH, TANK_HEIGHT = 55,40

HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','teste_A.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),270)

HULLS_2_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_B','Hull_02.png'))
HULLS_2 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),90)
##hulls##


WIDTH, HEIGHT = 1400,920

bullet_group = pygame.sprite.Group()

class bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.Surface((50,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

    def update(self):
        self.rect.x += 5
        

class Player():
    def __init__(self,X,Y,WIDTH,HEIGHT,COLOR,ID):
        self.x = X
        self.y = Y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.COLOR = COLOR
        self.ID = ID
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        self.VEL = 3

    def draw(self, WIN,ID):
        print(ID)
        if self.ID == 0:
            WIN.blit(HULLS_1,(self.x,self.y))
        elif self.ID == 1:
            WIN.blit(HULLS_2,(self.x,self.y))
        bullet_group.draw(WIN)
        #pygame.draw.rect(WIN, self.COLOR, self.rect)

    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.x - self.VEL > 0:  # LEFT
            self.x -= self.VEL
        if keys_pressed[pygame.K_d] and self.x + self.VEL + 50 < WIDTH: # RIGHT
            self.x += self.VEL
        if keys_pressed[pygame.K_w] and self.y - self.VEL > 0: # UP
            self.y -= self.VEL
        if keys_pressed[pygame.K_s] and self.y + self.VEL + 50 < HEIGHT: # DOWN
            self.y += self.VEL
        if keys_pressed[pygame.K_SPACE]: #FIRE
            bullet_group.add(self.create_bullet())
        
        bullet_group.update()
        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def create_bullet(self):
        return bullet(self.x,self.y)
