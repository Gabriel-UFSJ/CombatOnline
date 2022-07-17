import pickle
import random
import socket
import threading
from random import randint
from Player import Player
from pygame import mixer

#####SOUNDS#####
HIT_SOUND = mixer.Sound('Sounds/hit.wav')
################

WIDTH, HEIGHT = 1400,900

health = [3,3]

x = randint(0, 3)
y = randint(0, 3)
z = randint(0, 3)

game_map = [x, y, z]
CURRENT_PLAYER = [0, 1, 2, 3]      # Retornar a posição do player

# power ups
# power_info = [creation,pos_x,pos_y,type]

power_info = [False,0,0,0]

def spawn_powerup():
    power_info[0] = bool(random.choice([True, False]))
    power_info[1] = randint(0,1400)
    power_info[2] = randint(0,900)
    power_info[3] = randint(1,8)
    return power_info


# Players
players = [Player(60,380,0,health[0], game_map, power_info, right = True, left= False), Player(1100,380,1,health[1],game_map, power_info, right = False, left = True)]


#Hit verification
def hit(PLAYER1,PLAYER2):
    for bullet in PLAYER2.bullets:
        if PLAYER1.rect[0] < bullet.x < PLAYER1.rect[0] + PLAYER1.rect[2] and PLAYER1.rect[1] < bullet.y + 1 < PLAYER1.rect[1] + PLAYER1.rect[3]:
            if (PLAYER1.health > 0):
                HIT_SOUND.play()
                print("player1 lost health")
                health[0] -= 1
                PLAYER2.bullets.remove(bullet)
                return True

    for bullet in PLAYER1.bullets:
        if PLAYER2.rect[0] < bullet.x < PLAYER2.rect[0] + PLAYER2.rect[2] and PLAYER2.rect[1] < bullet.y + 1 < PLAYER2.rect[1] + PLAYER2.rect[3]:
            if (PLAYER1.health > 0):
                HIT_SOUND.play()
                print("player2 lost health")
                health[1] -= 1 
                PLAYER1.bullets.remove(bullet)
                return True
    return False

#item pickup verification
def testpickup(PLAYER1,PLAYER2):
    for powerups in PLAYER1.powers:
        if PLAYER1.rect[0] < powerups.x < PLAYER1.rect[0] + PLAYER1.rect[2] and PLAYER1.rect[1] < powerups.y + 1 < PLAYER1.rect[1] + PLAYER1.rect[3]:
            if len(PLAYER1.inventory) <= 5:
                print("p1 pickup")
                PLAYER1.inventory.append(powerups)
                PLAYER1.powers.remove(powerups)
    
    for powerups in PLAYER1.powers:
        if PLAYER2.rect[0] < powerups.x < PLAYER2.rect[0] + PLAYER2.rect[2] and PLAYER2.rect[1] < powerups.y + 1 < PLAYER2.rect[1] + PLAYER2.rect[3]:
            if len(PLAYER1.inventory) <= 5:
                print("p2 pickup")
                PLAYER1.inventory.append(powerups)
                PLAYER1.powers.remove(powerups)

#threading for client
def threaded_client(CONNECTION,PLAYER):
    global CURRENT_PLAYER
    power_number = 0
    CONNECTION.send(pickle.dumps(players[PLAYER]))
    REPLY = ""
    while True:
        try:

            DATA = pickle.loads(CONNECTION.recv(4096))
            players[PLAYER] = DATA
            players[PLAYER].health = health[PLAYER]
            players[PLAYER].power_info[0] = False

            if power_number <= 5:
                power_number += 1
                random_power = spawn_powerup()
                print(power_number)

            players[PLAYER].power_info = random_power

            testpickup(players[0], players[1])

            if hit(players[0], players[1]):

                players[0].rect.x = players[0].p_posx
                players[0].rect.y = players[0].p_posy

                players[1].rect.x = players[1].p_posx
                players[1].rect.y = players[1].p_posy

                players[PLAYER].start = True
            


            if not DATA:
                print("Disconnected")
                break
            else:
                REPLY = players
            CONNECTION.sendall(pickle.dumps(REPLY))
        except:
            break
    print("Connection lost")
    CURRENT_PLAYER.append(PLAYER)
    CONNECTION.close()


def main():
    global CURRENT_PLAYER
    SERVER = "localhost"
    PORT = 5555

    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SERVER_SOCKET.bind((SERVER, PORT))
    except socket.error as E:
        str(E)

    SERVER_SOCKET.listen(2)
    print("Server ready")
    print("Waiting for a connection")

    while True:
        CONNECTION, ADDR = SERVER_SOCKET.accept()
        print("Connected to: ", ADDR)

        if 0 in CURRENT_PLAYER:
            CURRENT_PLAYER.remove(0)
            threading.Thread(target=threaded_client, args=(CONNECTION, 0)).start()
        elif 1 in CURRENT_PLAYER:
            CURRENT_PLAYER.remove(1)
            threading.Thread(target=threaded_client, args=(CONNECTION, 1)).start()
        # elif 2 in CURRENT_PLAYER:                                                 # Adicionar quando aceitar 4 players
        #     print("Posição 2 ocupada")
        #     threading.Thread(target=threaded_client, args=(CONNECTION, 2)).start()
        #     CURRENT_PLAYER.remove(2)
        # elif 3 in CURRENT_PLAYER:
        #     print("Posição 3 ocupada")
        #     threading.Thread(target=threaded_client, args=(CONNECTION, 3)).start()
        #     CURRENT_PLAYER.remove(3)
        else:
            CONNECTION.close()
            print("Full session")
        print(CURRENT_PLAYER)

        # if len(CURRENT_PLAYER) <= 2:
        #     players.start = True

if __name__ == "__main__":
    main()
    
    
