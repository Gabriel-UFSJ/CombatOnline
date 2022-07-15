import pickle
import socket
import threading
from random import randint
from Player import Player
from pygame import mixer

#####SOUNDS#####
HIT_SOUND = mixer.Sound('Sounds/hit.wav')
# mixer.music.load('Sounds/backgroundMusic.wav')
# mixer.music.play(-1)
################

WIDTH, HEIGHT = 1400,900

health = [3,3]

x = randint(0, 4)
y = randint(0, 4)
z = randint(0, 4)

game_map = [x, y, z]
CURRENT_PLAYER = [0, 1, 2, 3]      # Retornar a posição do player

players = [Player(60,480,0,health[0], game_map, right = True, left= False), Player(900,480,1,health[1],game_map, right = False, left = True)]

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

def threaded_client(CONNECTION,PLAYER):
    global CURRENT_PLAYER

    CONNECTION.send(pickle.dumps(players[PLAYER]))
    REPLY = ""
    while True:
        try:
            DATA = pickle.loads(CONNECTION.recv(2048))
            players[PLAYER] = DATA
            players[PLAYER].health = health[PLAYER]
            
            if hit(players[0], players[1]):
                players[0].rect.move(players[0].p_posx,players[0].p_posy)

                players[1].rect.move(players[1].p_posx,players[1].p_posy)
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
    
    
