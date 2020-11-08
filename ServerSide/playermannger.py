
from .IActions import *
from random import randint
import os
import socket
import json
from threading import Thread, Lock
import pickle
import time

class PlayerMannger:
    def __init__(self,users):
        self.users=users
        self.semaphore =True


    def play(self,conn,user):
        while self.semaphore :
            if self.users[user['index']]['status']!=2 and self.users[user['index']]['status']!=1:
                self.sendaction(conn,Options())
                option= self.recv_option(conn)
                if option=="search":
                    self.sendaction(conn,WaitForOpponent())
                    self.searchgamestatus(user)
                    print(self.users[user['index']]['status']) 
                    time.sleep(3)





    def sendaction(sel,conn,action):
        encodeaction=pickle.dumps(action)
        conn.send(encodeaction)




                    
    def recv_option(self,sock):
        while True:
            option=sock.recv(1024).decode("ascii")
            if option:
                print(" \n the option is :",option)
                return option
                break  


    def searchgamestatus(self,user):
        self.users[user['index']]['status']=1
