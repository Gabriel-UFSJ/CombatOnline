import pickle
import traceback
import pygame
import os

##hulls##
TANK_WIDTH, TANK_HEIGHT = 55,40

HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','teste_A.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),270)

HULLS_2_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_B','Hull_02.png'))
HULLS_2 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),90)
##hulls##

##effects##
BULLET_IMAGE = pygame.image.load(os.path.join('Assets','PNG','Effects','Light_Shell.png'))
BULLET_LEFT = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),90)
BULLET_RIGHT  = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),270)

##effects##


WIDTH, HEIGHT = 1400,920


class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,pos_right, pos_left):
        self.x = pos_x
        self.y = pos_y
        self.right = pos_right
        self.left = pos_left

        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.color = (255,0,0)

    def draw_bullet(self, WIN):
        if self.right == True:
            WIN.blit(BULLET_RIGHT,(self.x,self.y))
        elif self.left == True:
            WIN.blit(BULLET_LEFT,(self.x,self.y))


    
    def update(self):
        if self.right == True:
            self.x += 5
        elif self.left == True:
            self.x -= 5


class Player():
    def __init__(self,X,Y,WIDTH,HEIGHT,COLOR,ID,right,left):
        self.x = X
        self.y = Y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.COLOR = COLOR
        self.ID = ID
        self.right = right
        self.left = left
        self.up = False
        self.down = False
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        self.VEL = 3
        self.bullets = []

    def draw_player(self, WIN):
        if self.right == True:
            WIN.blit(HULLS_1,(self.x,self.y))
        else:
            WIN.blit(HULLS_2,(self.x,self.y))

    def animation(self):
        global HULLS_1
        

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
            bullet = Bullet(self.x, self.y, self.right, self.left)
            self.bullets.append(bullet)  
        for bullet in self.bullets:
            Bullet.update(bullet)

        self.animation()
        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
