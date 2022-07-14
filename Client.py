import re
import pygame
import os
from Network import Network

WIDTH, HEIGHT = 1260,720

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
DISPLAY = pygame.Surface((1260,720))
pygame.display.set_caption("Combat Client")

FPS = 60

MYFONT = pygame.font.init()
MYFONT = pygame.font.Font(None, 100) 

###########Colors###########
WHITE = (255,255,255)
RED = (255,0,0)
CRIMSON = (220,20,60)
DARKRED = (139,0,0)
###########Assets###########

##tiles##
TILE_1_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'iron.png'))
TILE_2_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'iron_vent.png'))
TILE_3_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'cooper.png'))
TILE_4_IMAGE = pygame.image.load(os.path.join('Assets','TILES', 'night.png'))

TILE_SIZE = 36

TILE_1 = pygame.transform.rotate(pygame.transform.scale(TILE_1_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
TILE_2 = pygame.transform.rotate(pygame.transform.scale(TILE_2_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
TILE_3 = pygame.transform.rotate(pygame.transform.scale(TILE_3_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
TILE_4 = pygame.transform.rotate(pygame.transform.scale(TILE_4_IMAGE,(TILE_SIZE, TILE_SIZE)),0)
##tiles##

def draw_window(WIN, DISPLAY, PLAYER1, PLAYER2):
    DISPLAY.fill(DARKRED)

    draw_map(DISPLAY,PLAYER1.map)  
    SURF = pygame.transform.scale(DISPLAY, (WIDTH,HEIGHT))
    WIN.blit(SURF,(0,0))   

    for bullet in PLAYER1.bullets: #print bullets for player1
        bullet.draw_bullet(WIN)
    for bullet in PLAYER2.bullets: #print bullets for player2
        bullet.draw_bullet(WIN)

    PLAYER1.draw_player(WIN) #drawing player1
    PLAYER2.draw_player(WIN) #drawing player2

    PLAYER1_HEALTH = MYFONT.render(str(PLAYER1.health),1,(0,0,0))
    PLAYER2_HEALTH = MYFONT.render(str(PLAYER2.health),1,(0,0,0))
    WIN.blit(PLAYER1_HEALTH,(PLAYER1.p_posx,PLAYER1.p_posy - 470))
    WIN.blit(PLAYER2_HEALTH,(PLAYER2.p_posx,PLAYER2.p_posy - 470))
    
    #drawrect()

    pygame.display.update()

def start_round(WIN,PLAYER1,index):
    Start = [ '3', '2', '1', 'READY']
    #print(index)
    if PLAYER1.start == True: 
        ready = MYFONT.render(str(Start[index]),1,(0,0,0))
        WIN.blit(ready,(600,350))
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
                ['1','0','0','0','0',f'{x}','0','0',f'z','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}','0','0','0','0','1'],
                ['1','0','0','0','0',f'{x}','0','0',f'z','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}','0','0','0','0','1'],
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
                DISPLAY.blit(TILE_1 , (x * TILE_SIZE, y * TILE_SIZE))        
            if title == '2':
                DISPLAY.blit(TILE_2 , (x * TILE_SIZE, y * TILE_SIZE))
            if title == '3':
                DISPLAY.blit(TILE_3 , (x * TILE_SIZE, y * TILE_SIZE))
            if title == '4':
                DISPLAY.blit(TILE_4 , (x * TILE_SIZE, y * TILE_SIZE))
            if title != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,TILE_SIZE,TILE_SIZE))
            x += 1
        y += 1

def drawrect():
    for tiles in range(len(tile_rects)):
        pygame.draw.rect(WIN, (0,255,0), tile_rects[tiles])



def main():
    RUN = True
    
    NETWORK = Network() #create connection
    
    PLAYER1 = NETWORK.getServerPackage() #get connection for player1
    ID = PLAYER1.ID
    print(ID)
    i = 0
    CLOCK = pygame.time.Clock()

    while (RUN):
        CLOCK.tick(FPS)

        PLAYER1 = NETWORK.send(PLAYER1)[ID]

        if ID == 0:
            PLAYER2 = NETWORK.send(PLAYER1)[1] #send to server player1 and receive player2
        else:
            PLAYER2 = NETWORK.send(PLAYER1)[0] #send to server player1 and receive player2       
        #print(players)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()

        i = start_round(WIN,PLAYER1,i)
        PLAYER1.move()
        
        draw_window(WIN, DISPLAY, PLAYER1, PLAYER2)
            


if __name__ == "__main__":
    main()