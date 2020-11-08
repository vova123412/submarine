from .facadesubmaringame import *
from random import randint
import os
import socket
import json
from threading import Thread, Lock
import pickle
import time

class PreMatch:
    def __init__(self,users,threads):
        self.users=users
        self.threads=threads
        self.semaphore =True

    def threadfindmatch(self):
        matches= Thread(target=self.findmatch)
        self.threads.append(matches)
        matches.start()



    def findmatch(self):
        while self.semaphore :
            players_idx=self.searchforgames()
            if players_idx !=None:
                print(players_idx)
                self.changestatusingame(players_idx[0],players_idx[1])
                match=Thread(target=self.create_new_game,args=(players_idx[0],players_idx[1]))
                self.threads.append(match)
                match.start()



    def changestatusingame(self,player_one_idx,player_two_idx):
        self.users[player_one_idx]['status']=2
        self.users[player_two_idx]['status']=2


    def changestatusendgame(self,player_one_idx,player_two_idx):
        self.users[player_one_idx]['status']=0
        self.users[player_two_idx]['status']=0

    def create_new_game(self,player_one_idx,player_two_idx):
        one_vs_one=FacadeSubmarinGame(self.users[player_one_idx]['sock'],self.users[player_two_idx]['sock'],player_one_idx,player_two_idx,self)
        one_vs_one.startgame()
        

    def searchforgames(self):
        while self.semaphore :
            players_idx=[]
            for i in self.users:
                if i['status']==1:
                    players_idx.append(i['index'])
                if len(players_idx)==2:
                    print("match found")
                    return players_idx

