from sys import displayhook
from turtle import width
import pygame
import os
from Network import Network
from Player import Player

WIDTH, HEIGHT = 1400,900

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
DISPLAY = pygame.Surface((348,228))
pygame.display.set_caption("Combat Client")

CLIENTS = {}
FPS = 60

###########Colors###########
WHITE = (255,255,255)
RED = (255,0,0)
CRIMSON = (220,20,60)
DARKRED = (139,0,0)
###########Assets###########

##hulls##
TANK_WIDTH, TANK_HEIGHT = 55,55

HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','Hull_02.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(100, 100)),270)
##hulls##

##tiles##

TILE_1_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'iron.png'))
TILE_2_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'iron_vent.png'))
TILE_3_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'cooper.png'))
TILE_4_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'night.png'))

#TILE_SIZE = TILE_1_IMAGE.get_width()
TILE_SIZE = 12

TILE_1 = pygame.transform.rotate(pygame.transform.scale(TILE_1_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
TILE_2 = pygame.transform.rotate(pygame.transform.scale(TILE_2_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
TILE_3 = pygame.transform.rotate(pygame.transform.scale(TILE_3_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
TILE_4 = pygame.transform.rotate(pygame.transform.scale(TILE_4_IMAGE,(TILE_SIZE, TILE_SIZE)),0)



##tiles##

def draw_window(WIN, DISPLAY, PLAYER1, PLAYER2):
    DISPLAY.fill(DARKRED)
    draw_map(DISPLAY)  
    SURF = pygame.transform.scale(DISPLAY, (WIDTH,HEIGHT))
    WIN.blit(SURF,(0,0))
    PLAYER1.draw(WIN,PLAYER1.ID)
    PLAYER2.draw(WIN,PLAYER2.ID)
    pygame.display.update()

game_map = [['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','1','1','1','0','0','0','0','0','1','1','1','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','1'],
            ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1'],
            ['1','0','0','0','1','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','1','0','0','0','1'],
            ['1','0','0','0','1','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','1','0','0','0','1'],
            ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1'],
            ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1'],
            ['1','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','1','1','1','0','0','0','0','0','1','1','1','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

tile_rects = []

def draw_map(DISPLAY):
    y = 0
    for row in game_map:
        x = 0
        for title in row:
            if title == '1':
                DISPLAY.blit(TILE_1 , (x * TILE_SIZE, y * TILE_SIZE))
            if title == '2':
                DISPLAY.blit(TILE_2 , (x * TILE_SIZE, y * TILE_SIZE))
            if title != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,TILE_SIZE,TILE_SIZE))
            x += 1
        y += 1

def main():
    RUN = True
    
    NETWORK = Network()
    
    PLAYER1 = NETWORK.getPlayer()


    CLOCK = pygame.time.Clock()

    while (RUN):
        CLOCK.tick(FPS)
        PLAYER2 = NETWORK.send(PLAYER1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()

        #collisions = PLAYER1.collision(tile_rects)
        PLAYER1.move()


        draw_window(WIN, DISPLAY, PLAYER1, PLAYER2)  


if __name__ == "__main__":
    main()