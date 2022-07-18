import re
import pygame
import os
from Network import Network
from pygame import mixer

WIDTH, HEIGHT = 1260,720

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
DISPLAY = pygame.Surface((1260,720))
pygame.display.set_caption("Combat Client")

FPS = 60

pygame.font.init()
MYFONT = pygame.font.Font(None, 100) 

###########Colors###########
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CRIMSON = (220, 20, 60)
DARKRED = (139, 0, 0)
###########Assets###########

##tiles##
TILE_1_IMAGE = pygame.image.load(os.path.join('Assets', 'TILES', 'iron.png')).convert_alpha()
TILE_2_IMAGE = pygame.image.load(os.path.join('Assets', 'TILES', 'iron_vent.png')).convert_alpha()
TILE_3_IMAGE = pygame.image.load(os.path.join('Assets', 'TILES', 'cooper.png')).convert_alpha()
TILE_4_IMAGE = pygame.image.load(os.path.join('Assets', 'TILES', 'night.png')).convert_alpha()

TILE_SIZE = 36

TILE_1 = pygame.transform.rotate(pygame.transform.scale(TILE_1_IMAGE, (TILE_SIZE, TILE_SIZE)), 0)
TILE_2 = pygame.transform.rotate(pygame.transform.scale(TILE_2_IMAGE, (TILE_SIZE, TILE_SIZE)), 0)
TILE_3 = pygame.transform.rotate(pygame.transform.scale(TILE_3_IMAGE, (TILE_SIZE, TILE_SIZE)), 0)
TILE_4 = pygame.transform.rotate(pygame.transform.scale(TILE_4_IMAGE, (TILE_SIZE, TILE_SIZE)), 0)
##tiles##

#####SOUNDS#####
pygame.init()
POWERUP_SOUND = mixer.Sound('Sounds/powerup.wav')
mixer.music.load('Sounds/backgroundMusic.wav')
mixer.music.play(-1)
################


def draw_window(WIN, DISPLAY, PLAYER1, PLAYER2, PLAYER3, PLAYER4):
    DISPLAY.fill(DARKRED)

    draw_map(DISPLAY, PLAYER1.map)
    SURF = pygame.transform.scale(DISPLAY, (WIDTH, HEIGHT))
    WIN.blit(SURF, (0, 0))

    for bullet in PLAYER1.bullets:  # print bullets for player1
        bullet.draw_bullet(WIN)
    for bullet in PLAYER2.bullets:  # print bullets for player2
        bullet.draw_bullet(WIN)
    for bullet in PLAYER3.bullets:  # print bullets for player3
        bullet.draw_bullet(WIN)
    for bullet in PLAYER4.bullets:  # print bullets for player4
        bullet.draw_bullet(WIN)

    for powerup in PLAYER1.powers:
        powerup.draw_powerup(WIN)

    PLAYER1.draw_player(WIN)    #drawing player1

    if not PLAYER2.invisibility: PLAYER2.draw_player(WIN)    #drawing player2
    if not PLAYER3.invisibility: PLAYER3.draw_player(WIN)    #drawing player3
    if not PLAYER4.invisibility: PLAYER4.draw_player(WIN)    #drawing player4

    PLAYER1_HEALTH = MYFONT.render(str(PLAYER1.health), 1, (0, 0, 0))
    PLAYER2_HEALTH = MYFONT.render(str(PLAYER2.health), 1, (0, 0, 0))
    PLAYER3_HEALTH = MYFONT.render(str(PLAYER3.health), 1, (0, 0, 0))
    PLAYER4_HEALTH = MYFONT.render(str(PLAYER4.health), 1, (0, 0, 0))

    WIN.blit(PLAYER1_HEALTH, (115, 0))
    WIN.blit(PLAYER2_HEALTH, (430, 0))
    WIN.blit(PLAYER3_HEALTH, (745, 0))
    WIN.blit(PLAYER4_HEALTH, (1060, 0))

    
    #drawrect()

    pygame.display.update()

def start_round(WIN,PLAYER1,index):
    Start = ['3', '2', '1', 'READY    ']
    #print(index)
    if PLAYER1.start == True: 
        ready = MYFONT.render(str(Start[index]), 1, (0, 0, 0))
        WIN.blit(ready, (600, 350))
        pygame.display.update()
        pygame.time.delay(500)
        index += 1
        if index >= 4:
            PLAYER1.start = False
            return 0
        else:
            return index
    else:
        return 0


tile_rects = []

def draw_map(DISPLAY,game_map):
    x = game_map[0]
    y = game_map[1]
    z = game_map[2]


    
    game_map =  [
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0',f'{y}',f'{y}',f'{y}',f'{y}','0','0','0','0','0','0','0','0','0',f'{y}',f'{y}',f'{y}',f'{y}','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0',f'{x}',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}',f'{x}','0','0','0','1'],
                ['1','0','0','0','0',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}','0','0','0','0','1'],
                ['1','0','0','0','0',f'{x}','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0',f'{x}','0','0','0','0','1'],
                ['1','0','0','0','0',f'{x}','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0',f'{x}','0','0','0','0','1'],
                ['1','0','0','0','0',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}','0','0','0','0','1'],
                ['1','0','0','0',f'{x}',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}',f'{x}','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0',f'{y}',f'{y}',f'{y}',f'{y}','0','0','0','0','0','0','0','0','0',f'{y}',f'{y}',f'{y}',f'{y}','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
                ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
                ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
                ]

    y = 0
    for row in game_map:
        x = 0
        for title in row:
            if title == '1':
                DISPLAY.blit(TILE_1, (x * TILE_SIZE, y * TILE_SIZE))
            if title == '2':
                DISPLAY.blit(TILE_2, (x * TILE_SIZE, y * TILE_SIZE))
            if title == '3':
                DISPLAY.blit(TILE_3, (x * TILE_SIZE, y * TILE_SIZE))
            if title == '4':
                DISPLAY.blit(TILE_4, (x * TILE_SIZE, y * TILE_SIZE))
            if title != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

def drawrect():
    for tiles in range(len(tile_rects)):
        pygame.draw.rect(WIN, (0, 255, 0), tile_rects[tiles])



def main():
    RUN = True
    
    NETWORK = Network()                     # create connection
    
    PLAYER1 = NETWORK.getServerPackage()    # get connection for player1
    ID = PLAYER1.ID
    print(ID)
    print(PLAYER1)
    i = 0
    CLOCK = pygame.time.Clock()

    while RUN:
        index = [0,1,2,3]
        CLOCK.tick(FPS)

        players = NETWORK.send(PLAYER1)
        
        PLAYER1 = players[ID]

        index.remove(ID)

        PLAYER2 = players[index[0]]  # send to server player1 and receive player2
        PLAYER3 = players[index[1]]  # send to server player1 and receive player3
        PLAYER4 = players[index[2]]  # send to server player1 and receive player4    

        players = None 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()

        i = start_round(WIN, PLAYER1, i)

        PLAYER1.keys(tile_rects)
        PLAYER1.power_create(tile_rects)
        
        draw_window(WIN, DISPLAY, PLAYER1, PLAYER2, PLAYER3, PLAYER4)
            


if __name__ == "__main__":
    main()