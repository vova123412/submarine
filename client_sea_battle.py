import socket
import pickle
import time
import threading
from Actions.IActions import *

class Client():
    def __init__(self):   
        self.flag=True
        self.matrix= [0] * 100
        for i in range(9):
            self.matrix[i+1]=i+1
        for i in range(9):
            self.matrix[(i+1)*10]=i+1

        self.init_conn()

    def Print(self):
        Lmatrix =[ self.matrix[i:i+10] for i in range(0,len(self.matrix),10) ]
        for i in Lmatrix:
            print(i)
        

            
    def play(self,sock):
        location=0
        while self.flag:
            action_strategy=pickle.loads(sock.recv(1024))
            if action_strategy.do_action(sock)==0:
                break
        print("Game Over")


    def init_conn(self):
        threads=[]
        P_List=""
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 65432        # The port used by the server
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        t = threading.Thread(target=self.play,args=(sock,))
        threads.append(t)
        t.start()

   
client=Client()