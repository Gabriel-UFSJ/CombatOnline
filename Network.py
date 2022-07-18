import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create socket
        self.server = "172.18.1.7"                                           # bind server ip
        self.port = 5555                                                    # bind server port
        self.addr = (self.server, self.port)                                # set addr
        self.ServerPackage = self.connect()                                 # conection with the server
    
    def getServerPackage(self):
        return self.ServerPackage

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))   
        except socket.error as E:
            print(E)