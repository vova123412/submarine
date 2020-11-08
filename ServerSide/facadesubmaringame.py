
from random import randint
import os
import socket
from .prematch import *
from .IActions import *
import json
from threading import Thread, Lock
import pickle
import time

class FacadeSubmarinGame:
    def __init__(self,player_one_sock,player_two_sock,player_one_idx,player_two_idx,prematch):
        self.prematch=prematch
        self.player_idx=player_one_idx
        self.player2_idx=player_two_idx
        self.player_conn=player_one_sock
        self.player_map=[]
        self.player2_conn=player_two_sock
        self.player2_map=[]
        self.action={
        "Send_Ship":Send_Ship(),
        "Turn":Turn(),
        "Miss":Miss(),
        "Hit":Hit(),
        "Win":Win(),
        "Lose":Lose(),
        "Error":Error(),
        }



    def startgame(self):
        self.init_players_boards()
        self.playonevsone(self.player_conn,self.player_map,self.player2_conn,self.player2_map) 


    def init_players_boards(self):
        self.player_map= self.init_game_board(self.player_conn)
        self.player2_map=self.init_game_board(self.player2_conn)


    def init_game_board(self,conn):
        self.sendaction(conn,self.action["Send_Ship"])
        ship_array=pickle.loads(conn.recv(1024))
        while self.validate_game_board(ship_array)==False:
            self.sendaction(conn,self.action["Send_Ship"])
            ship_array=pickle.loads(conn.recv(1024))
        return ship_array


    def validate_game_board(self,ship_array):
        try:         
            for i in ship_array:
                print(type(i))
                if i<=9 or i>100 or (i>9 and i%10==0):
                    print("fail")
                    return False
            return True
        except:
                conn.send(self.action["Error"])
        return False



    # using connection objects is not hiding 3d-party code like sockets -> moved to IAction



    # this function is over 10 lines of code
    def playonevsone(self,sock,shiplist,sock2,shiplist2):
        print("\n \n",shiplist,shiplist2)
        while len(shiplist)!=0 and len(shiplist2)!=0:
            if self.turnplayer(sock,shiplist,sock2,shiplist2)==False:
                break
            if self.turnplayer(sock2,shiplist2,sock,shiplist)==False:
                break
        self.changestatusendgame(self.player2_idx,self.player_idx)


    # the function doesnt contain a verb
    def changestatusendgame(self,index,index2):
        self.prematch.changestatusendgame(index,index2)

    def turnplayer(self,sock,shiplist,sock2,shiplist2):
            self.sendaction(sock,self.action["Turn"])
            coordinate=int(self.recv_coordinate(sock))
            return self.replyaction(sock,shiplist,sock2,shiplist2,coordinate)


    def replyaction(self,sock,shiplist,sock2,shiplist2,coordinate):
        if self.searchinshiplist(coordinate,shiplist2):
            self.action["Hit"].set_coordinate(coordinate)
            self.sendaction(sock,self.action["Hit"])
            shiplist2.remove(coordinate)
            if(len(shiplist2)==0):
                self.sendaction(sock,self.action["Win"])
                self.sendaction(sock2,self.action["Lose"])
                return False
            return True
        self.action["Miss"].set_coordinate(coordinate)
        self.sendaction(sock,self.action["Miss"])
        return True





    def searchinshiplist(self,coordinate,shiplist):
        for i in shiplist:
            if coordinate == i:
                return True
        return False


    # decoding and encoding are low level abstraction
    def sendaction(self,conn,action):
        encodeaction=pickle.dumps(action)
        conn.send(encodeaction)



    def recv_coordinate(self,sock):
        while True:
            data=sock.recv(1024).decode("ascii")
            if data:
                print(" \n the data is :",data)
                return data
                break  
