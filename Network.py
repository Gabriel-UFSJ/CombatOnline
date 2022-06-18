import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.server = "26.202.88.100"           #bind server ip
        self.port = 5555                        #bind server port
        self.addr = (self.server,self.port)     #set addr
        self.player = self.connect()            #conection with the server
    
    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))

        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))   
        except socket.error as E:
            print(E) 