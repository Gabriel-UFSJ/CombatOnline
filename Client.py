from operator import truediv
from tkinter import Widget
import pygame
import os
import threading
import socket
import select

WIDTH, HEIGHT = 1600,900

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Combat Client")

clientNumber = 0



CLIENTS = {}
FPS = 60
TANK_WIDTH, TANK_HEIGHT = 55,40


###########Colors###########
WHITE = (255,255,255)
RED = (255,0,0)
CRIMSON = (220,20,60)
DARKRED = (139,0,0)


###########Assets###########

##hulls##
HULLS_1_IMAGE = pygame.image.load(os.path.join('JogoOnline','Assets','PNG', 'Hulls_Color_A','Hull_02.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),270)

##hulls##

class Player():
    def __init__(self,X,Y,WIDTH,HEIGHT,COLOR):
        self.x = X
        self.y = Y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.COLOR = COLOR
        self.rect = (X,Y,WIDTH,HEIGHT)
        self.VEL = 3

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.COLOR, self.rect)

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

        self.rect = (self.x,self.y, self.WIDTH, self.HEIGHT)

def draw_window(WIN, PLAYER):
    WIN.fill(DARKRED)
    PLAYER.draw(WIN)
    pygame.display.update()

def main():

    PLAYER = Player(100,430,TANK_WIDTH,TANK_HEIGHT,(0,255,0))

    clock = pygame.time.Clock()
    run = True

    while (run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        
        PLAYER.move()
        draw_window(WIN, PLAYER)
        
    pygame.quit()

if __name__ == "__main__":
    main()