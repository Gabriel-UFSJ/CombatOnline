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

def threaded_client(CONNECTION):
    CONNECTION.send(str.encode("Connected"))
    REPLY = ""
    while (True):
        try:
            DATA = CONNECTION.recv(2048)
            REPLY = DATA.decode("utf-8")
            if not DATA:
                print("Disconnected")
                break
            else:
                print("Recieved: ", REPLY)
                print("Sending : ", REPLY)

            CONNECTION.sendall(str.encode(REPLY))
        except:
            break
    print("Connection lost")
    CONNECTION.close()


while(True):
    CONNECTION, ADDR = SERVER_SOCKET.accept()
    print("Connected to: ", ADDR)

    threading.Thread(target=threaded_client, args = (CONNECTION,)).start()