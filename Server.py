import socket
import threading
import sys
from tkinter import E

SERVER = "192.168.5.110"
PORT = 5555

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SERVER_SOCKET.bind((SERVER,PORT))
except socket.error as E:
    str(E)

SERVER_SOCKET.listen(4)
print("Server ready")
print("Waiting for a connection")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

POS = [(0,0),(100,100),(200,200),(400,400)]

def threaded_client(CONNECTION,PLAYER):
    CONNECTION.send(str.encode(make_pos(POS[PLAYER])))
    REPLY = ""
    while (True):
        try:
            DATA = read_pos(CONNECTION.recv(2048).decode())
            POS[PLAYER] = DATA

            if not DATA:
                print("Disconnected")
                break
            else:
                if PLAYER == 1:
                    REPLY = POS[0]
                else:
                    REPLY = POS[1]     
                print("Recieved: ", DATA)
                print("Sending : ", REPLY)

            CONNECTION.sendall(str.encode(make_pos(REPLY)))
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