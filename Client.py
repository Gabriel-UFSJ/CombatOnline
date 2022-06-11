import pygame
import os
from Network import Network
from Player import Player

WIDTH, HEIGHT = 1600,900

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Combat Client")

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
HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','Hull_02.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),270)
##hulls##

def draw_window(WIN, PLAYER1,PLAYER2):
    WIN.fill(DARKRED)
    PLAYER1.draw(WIN)
    PLAYER2.draw(WIN)
    pygame.display.update()

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
        
        PLAYER1.move()
        draw_window(WIN, PLAYER1,PLAYER2)    


if __name__ == "__main__":
    main()