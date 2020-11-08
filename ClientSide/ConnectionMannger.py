        
from .SubmarinGame import *
import socket
import pickle
import time
import threading

class ConnectionMannger:
    def __init__(self,frame):
        self.value=""
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySubmarinGame=SubmarinGame(self.sock,frame)
        self.threads=[]
        self.HOST = '127.0.0.1' 
        self.PORT = 65432
        self.t=None



    def Init_Connection(self):
        self.sock.connect((self.HOST, self.PORT))
        

    

    def Play(self):
        self.t = threading.Thread(target=self.mySubmarinGame.Actions_loop,args=())
        self.threads.append(self.t)
        self.t.start()

