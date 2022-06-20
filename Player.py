import pickle
import traceback
import pygame
import os

##hulls##
TANK_WIDTH, TANK_HEIGHT = 55,40

HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','teste_A.png'))
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),0) # arrumar animações // hitbox

HULLS_2_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_B','Hull_02.png'))
HULLS_2 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),0) # arrumar animações // hitbox
##hulls##

##effects##
BULLET_IMAGE = pygame.image.load(os.path.join('Assets','PNG','Effects','Light_Shell.png'))
BULLET_LEFT = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),90)
BULLET_RIGHT  = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),270)

##effects##

WIDTH, HEIGHT = 1400,920


class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,look_right, look_left,look_up,look_down):
        self.x = pos_x
        self.y = pos_y
        self.right = look_right
        self.left = look_left
        self.up = look_up
        self.down = look_down

        self.rect = pygame.Rect(self.x, self.y, 50, 10)
        self.color = (255,0,0)

    def draw_bullet(self, WIN):
        self.rect = pygame.Rect(self.x, self.y + 20, 50, 10)
        pygame.draw.rect(WIN,(0,0,0),self.rect, 1)
        
        if self.right == True:
            WIN.blit(BULLET_RIGHT,(self.x,self.y - 25))
        elif self.left == True:
            WIN.blit(BULLET_LEFT,(self.x,self.y - 25))
    
    def update(self): #update de position of the bullet
        if self.right == True:
            self.x += 5
        elif self.left == True:
            self.x -= 5
        if self.up == True:
            self.y -= 5
        elif self.down == True:
            self.y += 5


    def off_screen(self): #return True if the bullet is of the screen
        return not(self.x >= 0 and self.x <= WIDTH)


class Player():
    def __init__(self,X,Y,ID,right,left):
        self.x = X
        self.y = Y
        self.WIDTH = TANK_WIDTH
        self.HEIGHT = TANK_HEIGHT
        self.ID = ID
        #look
        self.right = right
        self.left = left
        self.up = False
        self.down = False

        self.VEL = 1.5 #velocity of player
        #bullets
        self.bullets = [] #list of bullets
        self.cool_down_count = 0 #cool down for shooting
        #Health
        self.hitbox = (self.x + 5 ,self.y,TANK_WIDTH - 10,TANK_HEIGHT)
        self.health = 3
        print(self.health)

    def draw_player(self, WIN):
        self.hitbox = (self.x + 5 ,self.y,TANK_WIDTH - 10,TANK_HEIGHT)
        pygame.draw.rect(WIN,(0,0,0),self.hitbox, 1)
        
        if self.right == True:
            WIN.blit(HULLS_1,(self.x,self.y))
        else:
            WIN.blit(HULLS_2,(self.x,self.y))

    def move(self, player):
        global HULLS_1
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.x - self.VEL > 0:  # LEFT
            self.x -= self.VEL
            self.right = False
            self.left = True
            #HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),90)
        if keys_pressed[pygame.K_d] and self.x + self.VEL + 50 < WIDTH: # RIGHT
            self.x += self.VEL
            self.right = True
            self.left = False
            #HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),270)
        if keys_pressed[pygame.K_w] and self.y - self.VEL > 0: # UP
            self.y -= self.VEL
            self.up = True
            self.down = False
            #HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),0)
        if keys_pressed[pygame.K_s] and self.y + self.VEL + 50 < HEIGHT: # DOWN
            self.y += self.VEL
            self.up = False
            self.down = True
            #HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),180)
        self.shooting(player)
        self.update()

    def cooldown(self):
        if self.cool_down_count >= 60:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def shooting(self,player):
        self.hit(player)
        self.cooldown()
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE] and self.cool_down_count == 0: #FIRE
            bullet = Bullet(self.x, self.y, self.right, self.left, self.up, self.down)
            self.bullets.append(bullet) 
            self.cool_down_count = 1
        for bullet in self.bullets:
            Bullet.update(bullet)
            if(bullet.off_screen()):
                self.bullets.remove(bullet)

    def hit(self, player):
        for bullet in self.bullets:
            if player.hitbox[0] < bullet.x < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < bullet.y + 1 < player.hitbox[1] + player.hitbox[3]:
                if (player.health > 0):
                    player.health -= 1
            
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
