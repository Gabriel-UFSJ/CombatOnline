import pygame
import os
from pygame import mixer

#####SOUNDS#####
pygame.init()
SHOT_SOUND = mixer.Sound('Sounds/shot.wav')
HIT_SOUND = mixer.Sound('Sounds/hit.wav')
################

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

#####POWERUPS#####
POWERUP_SIZE = 36

POWERUP_1_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'armor.png'))            # Armadura extra
POWERUP_2_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'fastshot.png'))         # Tiro rápido
POWERUP_3_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'invincibility.png'))    # Invulnerabilidade
POWERUP_4_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'vel.png'))              # Movimento rápido
POWERUP_5_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'invisibility.png'))     # Invisibilidade
POWERUP_6_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'mult.png'))             # Tiro múltiplo
POWERUP_7_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'powerful.png'))         # Tiro poderoso
POWERUP_8_IMAGE = pygame.image.load(os.path.join('Assets', 'POWERUPS', 'weakening.png'))        # Tiro enfraquecedor

POWERUP_1 = pygame.transform.rotate(pygame.transform.scale(POWERUP_1_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_2 = pygame.transform.rotate(pygame.transform.scale(POWERUP_2_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_3 = pygame.transform.rotate(pygame.transform.scale(POWERUP_3_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_4 = pygame.transform.rotate(pygame.transform.scale(POWERUP_4_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_5 = pygame.transform.rotate(pygame.transform.scale(POWERUP_5_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_6 = pygame.transform.rotate(pygame.transform.scale(POWERUP_6_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_7 = pygame.transform.rotate(pygame.transform.scale(POWERUP_7_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
POWERUP_8 = pygame.transform.rotate(pygame.transform.scale(POWERUP_8_IMAGE, (POWERUP_SIZE, POWERUP_SIZE)), 0)
################

WIDTH, HEIGHT = 1400, 920

def collision_test(rect,tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list



class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,look_right, look_left):
        self.x = pos_x + 20
        self.y = pos_y + 17
        self.right = look_right
        self.left = look_left


        self.rect = pygame.Rect(self.x, self.y, 15, 10)
        self.color = (255,0,0)

    def draw_bullet(self, WIN):
        self.rect = pygame.Rect(self.x, self.y, 15, 10)
        #pygame.draw.rect(WIN,(0,0,0),self.rect, 1)
        
        if self.right == True:
            WIN.blit(BULLET_RIGHT,(self.x - 55,self.y - 45))
        elif self.left == True:
            WIN.blit(BULLET_LEFT, (self.x - 55,self.y - 45))
    
    def update(self): #update de position of the bullet
        if self.right == True:
            self.movement = 5
        elif self.left == True:
            self.movement = -5


    def off_screen(self): #return True if the bullet is of the screen
        return not(self.x >= 0 and self.x <= WIDTH)
        
    def colision(self,tiles):
        self.x += self.movement
        hit_list = collision_test(self.rect,tiles)

        for tile in hit_list:
            if self.movement > 0:
                self.rect.right = tile.left
                return True
            elif self.movement < 0:
                self.rect.left = tile.right
                return True
            else:
                return False

        


class Player():
    def __init__(self,X,Y,ID,health,map,right,left):
        self.ID = ID
        #placar
        self.p_posx = X
        self.p_posy = Y
        #mov
        self.movement = [0, 0]
        self.VEL = 1.5 #velocity of player
        self.right = right
        self.left = left
        self.up = False
        self.down = False
        #bullets
        self.bullets = [] #list of bullets
        self.cool_down_count = 0 #cool down for shooting
        #Health
        self.rect = pygame.Rect(X,Y,HULLS_1.get_width() ,HULLS_1.get_height())
        self.health = health
        #map
        self.map = map
        #server fill
        self.start = False
        
    def draw_player(self, WIN):
        #pygame.draw.rect(WIN,(0,0,0),self.rect,1)

        if self.right == True:
            WIN.blit(HULLS_1, (self.rect.x, self.rect.y))
        else:
            WIN.blit(HULLS_2, (self.rect.x, self.rect.y))

    def move(self,tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.movement[0]
        hit_list = collision_test(self.rect,tiles)

        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True

        self.rect.y += self.movement[1]
        hit_list = collision_test(self.rect,tiles)

        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return self.rect


    def keys(self,tile_rects):
        self.movement = [0, 0]
        global HULLS_1
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.rect.x - self.VEL > 0 :  # LEFT
            self.movement[0] = -self.VEL
        if keys_pressed[pygame.K_d] and self.rect.x + self.VEL + 50 < WIDTH: # RIGHT
            self.movement[0] = self.VEL
        if keys_pressed[pygame.K_w] and self.rect.y - self.VEL > 0  : # UP
            self.movement[1] = -self.VEL
        if keys_pressed[pygame.K_s] and self.rect.y + self.VEL + 50 < HEIGHT : # DOWN
            self.movement[1] = self.VEL
        
        self.rect = self.move(tile_rects)
        self.shooting(tile_rects)

    def cooldown(self):
        if self.cool_down_count >= 60:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def shooting(self,tiles):
        self.cooldown()
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE] and self.cool_down_count == 0: #FIRE
            SHOT_SOUND.play()
            bullet = Bullet(self.rect.x, self.rect.y,self.right,self.left)
            self.bullets.append(bullet) 
            self.cool_down_count = 1
        for bullet in self.bullets:
            Bullet.update(bullet)
            if(bullet.colision(tiles)):
                HIT_SOUND.play()
                self.bullets.remove(bullet)
            if(bullet.off_screen()):
                self.bullets.remove(bullet)


class POWERUP(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        global POWERUP_SIZE
        self.x = pos_x
        self.y = pos_y
        self.rect = pygame.Rect(self.x, self.y, POWERUP_SIZE, POWERUP_SIZE)
        self.color = (255, 0, 0)

    def draw_powerup(self, WIN):
        self.rect = pygame.Rect(self.x, self.y, POWERUP_SIZE, POWERUP_SIZE)
        WIN.blit(POWERUP_1, (self.x, self.y))

    # def colision(self, tiles):
    #     self.x += self.movement
    #     hit_list = collision_test(self.rect, tiles)
    #
    #     for tile in hit_list:
    #         if self.movement > 0:
    #             self.rect.right = tile.left
    #             return True
    #         elif self.movement < 0:
    #             self.rect.left = tile.right
    #             return True
    #         else:
    #             return False
