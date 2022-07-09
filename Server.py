import pickle
import socket
import threading
from random import randint
from Player import Player

WIDTH, HEIGHT = 1400,900

health = [3,3]

x = randint(0, 4)
y = randint(0, 4)
z = randint(0, 4)

game_map = [x,y,z]

players = [Player(60,480,0,health[0], game_map, right = True, left= False, start = False),Player(900,480,1,health[1],game_map, right = False, left = True, start = False)]

def hit(PLAYER1,PLAYER2):
    #print("testing")
    for bullet in PLAYER2.bullets:
        if PLAYER1.hitbox[0] < bullet.x < PLAYER1.hitbox[0] + PLAYER1.hitbox[2] and PLAYER1.hitbox[1] < bullet.y + 1 < PLAYER1.hitbox[1] + PLAYER1.hitbox[3]:
            if (PLAYER1.health > 0):
                print("player1 lost health")
                health[0] -= 1
                PLAYER2.bullets.remove(bullet)
                return True

    for bullet in PLAYER1.bullets:
        if PLAYER2.hitbox[0] < bullet.x < PLAYER2.hitbox[0] + PLAYER2.hitbox[2] and PLAYER2.hitbox[1] < bullet.y + 1 < PLAYER2.hitbox[1] + PLAYER2.hitbox[3]:
            if (PLAYER1.health > 0):
                print("player2 lost health")
                health[1] -= 1 
                PLAYER1.bullets.remove(bullet)
                return True
    return False

def threaded_client(CONNECTION,PLAYER):
    CONNECTION.send(pickle.dumps(players[PLAYER]))
    REPLY = ""
    while (True):
        try:
            DATA = pickle.loads(CONNECTION.recv(2048))
            players[PLAYER] = DATA
            players[PLAYER].health = health[PLAYER]
            
            if hit(players[0],players[1]):
                players[0].x = players[0].p_posx
                players[0].y = players[0].p_posy

                players[1].x = players[1].p_posx
                players[1].y = players[1].p_posy
                players.start = True

            if not DATA:
                print("Disconnected")
                break
            else:
                REPLY = players
            CONNECTION.sendall(pickle.dumps(REPLY))
            #print(players)
        except:
            break
    print("Connection lost")
    CONNECTION.close()

def main():
    SERVER = "26.202.88.100"
    PORT = 5555

    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SERVER_SOCKET.bind((SERVER,PORT))
    except socket.error as E:
        str(E)

    CURRENT_PLAYER = 0
    SERVER_SOCKET.listen(2)
    print("Server ready")
    print("Waiting for a connection")

    while True:
        #hit(players[0],players[1])
        CONNECTION, ADDR = SERVER_SOCKET.accept()
        print("Connected to: ", ADDR)
        print(CURRENT_PLAYER)
        threading.Thread(target=threaded_client, args = (CONNECTION,CURRENT_PLAYER)).start()
        CURRENT_PLAYER += 1
        if CURRENT_PLAYER >= 2:
            players.start = True

if __name__ == "__main__":
    main()
    
    
