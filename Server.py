import pickle
import socket
import threading
from random import randint
from Player import Player

WIDTH, HEIGHT = 1400,900

health1 = 3
health2 = 3



x = randint(0, 4)
y = randint(0, 4)
z = randint(0, 4)

game_map =  [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0',f'{y}',f'{y}',f'{y}','0','0','0','0','0',f'{y}',f'{y}',f'{y}','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','1'],
            ['1','0','0',f'{x}',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}',f'{x}','0','0','1'],
            ['1','0','0','0',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}','0','0','0','1'],
            ['1','0','0','0',f'{x}','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0',f'{x}','0','0','0','1'],
            ['1','0','0','0',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}','0','0','0','1'],
            ['1','0','0',f'{x}',f'{x}','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{x}',f'{x}','0','0','1'],
            ['1','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','0',f'{y}','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0',f'{y}',f'{y}',f'{y}','0','0','0','0','0',f'{y}',f'{y}',f'{y}','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0',f'{z}','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]


players = [Player(60,480,0,health1, game_map, right = True, left= False),Player(900,480,1,health2,game_map, right = False, left = True)]

def hit(PLAYER1,PLAYER2):
    #print("testing")
    for bullet in PLAYER2.bullets:
        if PLAYER1.hitbox[0] < bullet.x < PLAYER1.hitbox[0] + PLAYER1.hitbox[2] and PLAYER1.hitbox[1] < bullet.y + 1 < PLAYER1.hitbox[1] + PLAYER1.hitbox[3]:
            if (PLAYER1.health > 0):
                print("player1 lost health")
                PLAYER1.health -= 1 
                PLAYER1.x = PLAYER1.p_posx
                PLAYER1.y = PLAYER1.p_posy
                PLAYER2.bullets.remove(bullet)
    
    for bullet in PLAYER1.bullets:
        if PLAYER2.hitbox[0] < bullet.x < PLAYER2.hitbox[0] + PLAYER2.hitbox[2] and PLAYER2.hitbox[1] < bullet.y + 1 < PLAYER2.hitbox[1] + PLAYER2.hitbox[3]:
            if (PLAYER1.health > 0):
                print("player2 lost health")
                PLAYER2.health -= 1 
                PLAYER2.x = PLAYER2.p_posx
                PLAYER2.y = PLAYER2.p_posy
                PLAYER1.bullets.remove(bullet)

def threaded_client(CONNECTION,PLAYER):
    CONNECTION.send(pickle.dumps(players[PLAYER]))
    REPLY = ""
    while (True):
        try:
            DATA = pickle.loads(CONNECTION.recv(2048))
            players[PLAYER] = DATA
            hit(players[0],players[1])
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
        
if __name__ == "__main__":
    main()
    
    
