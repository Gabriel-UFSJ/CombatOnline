import socket
import threading
import sys
from tkinter import E

SERVER = ""
PORT = 5555

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SERVER_SOCKET.bind((SERVER,PORT))
except socket.error as E:
    str(E)

SERVER_SOCKET.listen(4)
print("Server ready")
print("waiting for a connection")

def threaded_client(CONNECTION):
    pass


while(True):
    CONNECTION, ADDR = SERVER_SOCKET.accept()
    print("Connected to: ", ADDR)

    threading.Thread(target=threaded_client, args = (CONNECTION,)).start()