from random import randint
import os
import socket
import json
from threading import Thread, Lock
import pickle
import time
from ServerSide.IActions import *
from ServerSide.playermannger import *
from ServerSide.prematch import *

# what is this proxy for?
# please revisit proxy pattern 
# maybe you could use a validator layer like decorato
    
    # this function is over 10 lines of code        

# Game Facade, but what game are we playing?

# what server?
class SocketMannager:
    # the constructor is over 10 lines of code
    def __init__(self):
        self.users=[]
        self.threads=[]
        HOST = '0.0.0.0'  
        PORT = 65432      
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(5)
        self.playermannger=PlayerMannger(self.users)
        self.prematch=PreMatch(self.users,self.threads)
    

    def acceptplayers(self):
        player_idx=0
        while player_idx<5: 
            conn, addr = self.sock.accept()
            user={
                'status':0,
                'index':player_idx,
                'addr':addr,
                'sock':conn,
                }
            player_idx=player_idx+1
            self.users.append(user)
            self.threadplayermannger(conn,user)

        self.semaphore =False
        sys.exit() 
    
    def threadplayermannger(self,conn,user):
        t = Thread(target=self.playermannger.play,args=(conn,user))
        self.threads.append(t)
        t.start()






def main():
    socketmannager=SocketMannager()
    socketmannager.prematch.threadfindmatch()
    socketmannager.acceptplayers()




if __name__ == "__main__":
    main()

        













