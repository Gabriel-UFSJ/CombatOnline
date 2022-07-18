from time import time
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
WEAPON_WIDTH, WEAPON_HEIGHT = 30,50

HULLS_1_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_A','teste_A.png'))
HULLS_1_WEAPON = pygame.image.load(os.path.join('Assets','PNG', 'Weapon_Color_A','Gun_07.png'))

WEAPON_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_WEAPON,(WEAPON_WIDTH, WEAPON_HEIGHT)),0)
HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),0) # arrumar animações // hitbox

HULLS_2_IMAGE = pygame.image.load(os.path.join('Assets','PNG', 'Hulls_Color_B','Hull_02.png'))
HULLS_2_WEAPON = pygame.image.load(os.path.join('Assets','PNG', 'Weapon_Color_B','Gun_07.png'))

WEAPON_2 = pygame.transform.rotate(pygame.transform.scale(HULLS_2_WEAPON,(WEAPON_WIDTH, WEAPON_HEIGHT)),0)
HULLS_2 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE,(TANK_WIDTH, TANK_HEIGHT)),0) # arrumar animações // hitbox
##hulls##

##effects##
BULLET_IMAGE = pygame.image.load(os.path.join('Assets','PNG','Effects','Light_Shell.png'))
BULLET_UP = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),0)
BULLET_LEFT = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),90)
BULLET_DOWN = pygame.transform.rotate(pygame.transform.scale(BULLET_IMAGE,(100,100)),180)
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

powerlist = [POWERUP_1,POWERUP_2,POWERUP_3,POWERUP_4,POWERUP_5,POWERUP_6,POWERUP_7,POWERUP_8]
################

WIDTH, HEIGHT = 1400, 920

def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list



class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, look_right, look_left,look_up, look_down,fast_shoot,power_shoot):
        self.x = pos_x + 20
        self.y = pos_y + 17
        self.right = look_right
        self.left = look_left
        self.up = look_up
        self.down = look_down

        self.fast_shoot = fast_shoot
        self.power_shoot = power_shoot
        self.movement = [0,0]

        self.rect = pygame.Rect(self.x, self.y, 15, 10)
        self.color = (255,0,0)

    def draw_bullet(self, WIN):
        self.rect = pygame.Rect(self.x, self.y, 15, 10)
        #pygame.draw.rect(WIN,(0,0,0),self.rect, 1)
        
        if self.right == True:
           WIN.blit(BULLET_RIGHT,(self.x - 40 ,self.y -45))
        elif self.left == True:
            WIN.blit(BULLET_LEFT, (self.x - 40 ,self.y -45))
        elif self.up == True:
            WIN.blit(BULLET_UP, (self.x - 40 ,self.y -45))
        elif self.down == True:
            WIN.blit(BULLET_DOWN, (self.x - 40 ,self.y -45))


    
    def update(self): #update de position of the bullet
        if self.right == True:
            if self.fast_shoot:
                self.movement[0] = 10
            else:
                self.movement[0] = 5

        elif self.left == True:
            if self.fast_shoot:
                self.movement[0] = -10
            else:
                self.movement[0] = -5

        elif self.down == True:
            if self.fast_shoot:
                self.movement[1] = 10
            else:
                self.movement[1] = 5

        elif self.up == True:
            if self.fast_shoot:
                self.movement[1] = -10
            else:
                self.movement[1] = -5
        


    def off_screen(self): #return True if the bullet is of the screen
        return not(self.x >= 0 and self.x <= WIDTH)
        
    def colision(self,tiles):
        self.x += self.movement[0]

        if not self.power_shoot: 
            hit_list = collision_test(self.rect,tiles)
        if hit_list:

            for tile in hit_list:
                if self.movement[0] > 0:
                    self.rect.right = tile.left
                    return True
                elif self.movement[0] < 0:
                    self.rect.left = tile.right
                    return True

        self.y += self.movement[1]
        
        if not self.power_shoot: 
            hit_list = collision_test(self.rect,tiles)
        if hit_list:

            for tile in hit_list:
                if self.movement[1] > 0:
                    print("colide")
                    self.rect.bottom = tile.top
                    return True
                elif self.movement[1] < 0:
                    print("colide")
                    self.rect.top = tile.bottom
                    return True
        return False

        


class Player():
    def __init__(self, X, Y, ID, health, map, power_info, right, left, up, down):
        self.ID = ID
        #placar
        self.p_posx = X
        self.p_posy = Y
        #mov
        self.movement = [0, 0]
        self.VEL = 1.5              # velocity of player
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        #bullets
        self.bullets = []           # list of bullets
        self.cool_down_count = 0    # cool down for shooting
        #Health
        self.rect = pygame.Rect(X, Y, HULLS_1.get_width(), HULLS_1.get_height())
        self.health = health
        self.dead = False
        #map
        self.map = map
        #server fill
        self.start = False
        #powerups
        self.power_info = power_info
        self.powers = []
        self.inventory = []
        #powers
        self.cool_down_item = 0
        self.extra_armor = False
        self.fast_shoot = False
        self.invulnerable = False
        self.move_fast = False
        self.invisibility = False
        self.multi_shoot = False
        self.power_shoot = False
        self.weakening_shoot = False
        
    def draw_player(self, WIN):
        centro = self.rect.center
        hulls1 = HULLS_1.get_rect(center = centro)

        #pygame.draw.rect(WIN,(0,0,0),self.rect, 1)
        WIN.blit(HULLS_1, hulls1)




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
        global HULLS_1, WEAPON_1
        keys_pressed = pygame.key.get_pressed()
        self.use_item()

        if self.move_fast:
            self.VEL = 2.5
        else:
            self.VEL = 1.5

        if keys_pressed[pygame.K_a] and self.rect.x - self.VEL > 0 :  # LEFT
            self.movement[0] = -self.VEL
            HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 90)
            WEAPON_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_WEAPON,(WEAPON_WIDTH, WEAPON_HEIGHT)),90)

            self.right = False
            self.left = True
            self.up = False
            self.down = False

        if keys_pressed[pygame.K_d] and self.rect.x + self.VEL + 50 < WIDTH: # RIGHT
            self.movement[0] = self.VEL
            HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 270)
            WEAPON_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_WEAPON,(WEAPON_WIDTH, WEAPON_HEIGHT)),270)

            self.right = True
            self.left = False
            self.up = False
            self.down = False

        if keys_pressed[pygame.K_w] and self.rect.y - self.VEL > 0  : # UP
            self.movement[1] = -self.VEL
            HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 360)
            WEAPON_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_WEAPON,(WEAPON_WIDTH, WEAPON_HEIGHT)),360)

            self.right = False
            self.left = False
            self.up = True
            self.down = False

        if keys_pressed[pygame.K_s] and self.rect.y + self.VEL + 50 < HEIGHT : # DOWN
            self.movement[1] = self.VEL
            HULLS_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 180)
            WEAPON_1 = pygame.transform.rotate(pygame.transform.scale(HULLS_1_WEAPON,(WEAPON_WIDTH, WEAPON_HEIGHT)),180)

            self.right = False
            self.left = False
            self.up = False
            self.down = True
        
        self.rect = self.move(tile_rects)
        self.shooting(tile_rects)


    def cooldown(self):
        if self.cool_down_count >= 60:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1
    
    def cooldown_item(self):
        if self.cool_down_item >= 180:
            self.cool_down_item = 0

            #reset itens
            self.extra_armor = False
            self.fast_shoot = False
            self.invulnerable = False
            self.move_fast = False
            self.invisibility = False
            self.multi_shoot = False
            self.power_shoot = False
            self.weakening_shoot = False

        elif self.cool_down_item > 0:
            self.cool_down_item += 1


    def use_item(self):
        self.cooldown_item()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_e] and self.cool_down_count == 0: #FIRE
            pos = len(self.inventory) - 1
            if self.inventory:
                print(self.inventory[pos].type)
                if self.inventory[pos].type == 1: # Armadura extra
                    print("armor")
                    self.extra_armor = True
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 2: # Tiro rápido
                    self.fast_shoot = True
                    print("fast_shoot")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 3: # Invulnerabilidade
                    self.invulnerable = True
                    print("invu")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 4: # Movimento rápido
                    self.move_fast = True
                    print("move_fast")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 5: # Invisibilidade
                    self.invisibility = True
                    print("invisivel")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 6: # Tiro múltiplo
                    self.multi_shoot = True
                    print("multi shoot")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 7: # Tiro poderoso
                    self.power_shoot = True
                    print("power shot")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1

                elif self.inventory[pos].type == 8: # Tiro enfraquecedor
                    self.weakening_shoot = True
                    print("tiro enfrac")
                    self.inventory.remove(self.inventory[pos])
                    self.cool_down_count = 1
            else:
                print("inventory empty")

    def shooting(self,tiles):
        self.cooldown()
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_SPACE] and self.cool_down_count == 0: #FIRE
            SHOT_SOUND.play()
            bullet = Bullet(self.rect.x, self.rect.y,self.right,self.left,self.up,self.down,self.fast_shoot,self.power_shoot)
            self.bullets.append(bullet) 
            self.cool_down_count = 1
            if self.multi_shoot:
                bullet = Bullet(self.rect.x, self.rect.y,self.right,self.left,self.up,self.down,self.fast_shoot,self.power_shoot)
                self.bullets.append(bullet) 
                bullet = Bullet(self.rect.x, self.rect.y,self.right,self.left,self.up,self.down,self.fast_shoot,self.power_shoot)
                self.bullets.append(bullet) 
                self.cool_down_count = 1
                
        for bullet in self.bullets:
            Bullet.update(bullet)
            if(bullet.colision(tiles)):
                HIT_SOUND.play()
                self.bullets.remove(bullet)
            if(bullet.off_screen()):
                self.bullets.remove(bullet)

    def power_create(self,tiles):
        if self.power_info[0] == True:
            x = int(self.power_info[1])
            y = int(self.power_info[2])
            rect = pygame.Rect(x,y,POWERUP_SIZE ,POWERUP_SIZE)
            hit_list = collision_test(rect, tiles)
            if not hit_list:
                print("create")
                power = POWERUP(self.power_info[1],self.power_info[2],self.power_info[3])
                self.powers.append(power)


class POWERUP():
    def __init__(self, pos_x, pos_y,power_type):
        global POWERUP_SIZE
        self.x = pos_x
        self.y = pos_y
        self.type = power_type
        self.rect = pygame.Rect(self.x, self.y, POWERUP_SIZE, POWERUP_SIZE)
        self.color = (255, 0, 0)

    def draw_powerup(self, WIN):
        #pygame.draw.rect(WIN,(0,0,0),self.rect,1)
        WIN.blit(powerlist[self.type - 1], (self.x, self.y))
    