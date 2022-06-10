import pygame
import os
from Network import Network


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
HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','Hull_02.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),270)

##hulls##

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

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def draw_window(WIN, PLAYER1,PLAYER2):
    WIN.fill(DARKRED)
    PLAYER1.draw(WIN)
    PLAYER2.draw(WIN)
    pygame.display.update()

def main():
    NETWORK = Network()
    STARTPOS = read_pos(NETWORK.getPos())

    PLAYER1 = Player(STARTPOS[0],STARTPOS[1],TANK_WIDTH,TANK_HEIGHT,(0,255,0))
    PLAYER2 = Player(0,0,TANK_WIDTH,TANK_HEIGHT,(0,255,0))

    CLOCK = pygame.time.Clock()
    RUN = True

    while (RUN):
        CLOCK.tick(FPS)

        PLAYER2_POS = read_pos(NETWORK.send(make_pos((PLAYER1.x,PLAYER1.y))))
        PLAYER2.X = PLAYER2_POS[0]
        PLAYER2.Y = PLAYER2_POS[1]
        PLAYER2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()
        
        PLAYER1.move()
        draw_window(WIN, PLAYER1,PLAYER2)    


if __name__ == "__main__":
    main()