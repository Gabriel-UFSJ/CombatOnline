import pickle
import socket
import threading
from Player import Player

WIDTH, HEIGHT = 1400,900

SERVER = "localhost"
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

players = [Player(60,480,CURRENT_PLAYER, right = True, left= False),Player(900,480,CURRENT_PLAYER,right = False, left = True)]

def threaded_client(CONNECTION,PLAYER):
    CONNECTION.send(pickle.dumps(players[PLAYER]))
    REPLY = ""
    while (True):
        try:
            DATA = pickle.loads(CONNECTION.recv(2048))
            players[PLAYER] = DATA

            if not DATA:
                print("Disconnected")
                break
            else:
                if PLAYER == 1:
                    REPLY = players[0]
                else:
                    REPLY = players[1]     
            CONNECTION.sendall(pickle.dumps(REPLY))
        except:
            break
    print("Connection lost")
    CONNECTION.close()


while True:
    CONNECTION, ADDR = SERVER_SOCKET.accept()
    print("Connected to: ", ADDR)
    print(CURRENT_PLAYER)
    threading.Thread(target=threaded_client, args = (CONNECTION,CURRENT_PLAYER)).start()
    CURRENT_PLAYER += 1
    
