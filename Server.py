import pickle
import socket
import threading
from Player import Player

SERVER = "26.202.88.100"
PORT = 5555

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SERVER_SOCKET.bind((SERVER,PORT))
except socket.error as E:
    str(E)

SERVER_SOCKET.listen(2)
print("Server ready")
print("Waiting for a connection")

players = [Player(0,0,50,50(255,0,0)),Player(100,100,50,50,(0,0,255))]

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
                print("Recieved: ", DATA)
                print("Sending : ", REPLY)

            CONNECTION.sendall(pickle.dumps(REPLY))
        except:
            break
    print("Connection lost")
    CONNECTION.close()

CURRENT_PLAYER = 0

while(True):
    CONNECTION, ADDR = SERVER_SOCKET.accept()
    print("Connected to: ", ADDR)

    threading.Thread(target=threaded_client, args = (CONNECTION,CURRENT_PLAYER)).start()
    CURRENT_PLAYER += 1