from random import randint
from threading import Thread, Lock
from Actions.IActions import *
import os
import socket
import json
import pickle
import time
import sys
class Server():
    def __init__(self):
        self.users=[]
        self.threads=[]
        self.init_server_flag=True
        HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(5)
        matches= Thread(target=self.match)
        self.threads.append(matches)
        matches.start()
        index=0
        while index<5: 
            conn, addr = sock.accept()
            print('Connected by', addr)
            user={
                'status':0,
                'index':index,
                'addr':addr,
                'sock':conn,
                }
            index=index+1
            self.users.append(user)
            t = Thread(target=self.play,args=(conn,user))
            self.threads.append(t)
            t.start()
        self.init_server_flag=False
        sys.exit() 




    def match(self):
        while self.init_server_flag:
            players_idx=self.searchforgames()
            if players_idx !=None:
                print(players_idx)
                self.statusingame(players_idx[0],players_idx[1])
                match=Thread(target=self.create_new_game,args=(players_idx[0],players_idx[1]))
                self.threads.append(match)
                match.start()

    def statusingame(self,player_one_idx,player_two_idx):
        self.users[player_one_idx]['status']=2
        self.users[player_two_idx]['status']=2
        

    def create_new_game(self,player_one_idx,player_two_idx):
        one_vs_one=Game(self.users[player_one_idx]['sock'],self.users[player_two_idx]['sock'])
        

    def searchforgames(self):
        while self.init_server_flag:
            players_idx=[]
            for i in self.users:
                if i['status']==1:
                    players_idx.append(i['index'])
                if len(players_idx)==2:
                    print("match found")
                    return players_idx


                
                   
        


    def play(self,conn,user):
        message=pickle.dumps(Options())
        conn.send(message)
        data= self.recv_data(conn)
        print(data)
        if data=="search" and self.users[user['index']]['status']!=2:
            self.searchgamestatus(user)
    def recv_data(self,sock):
        flag=True
        while flag:
            data=sock.recv(1024).decode("ascii")
            if data:
                print(" \n the data is :",data)
                return data
                break  


    def searchgamestatus(self,user):
        self.users[user['index']]['status']=1
        
    def wait(self,index,sock):
        pass
        
    

    



class Game():
    def  __init__(self,player_conn,player2_conn):
        self.player_conn=player_conn
        self.player_map=[]
        self.player2_conn=player2_conn
        self.player2_map=[]
        self.action={
        "Init_Ship":pickle.dumps(Init_Ship()),
        "Turn":pickle.dumps(Turn()),
        "Miss":Miss(),
        "Hit":Hit(),
        "Win":pickle.dumps(Win()),
        "Lose":pickle.dumps(Lose()),
        "Error":pickle.dumps(Error())
        }
        self.player_map= self.init_game_board(self.player_conn)
        self.player2_map=self.init_game_board(self.player2_conn)
        self.in_game(self.player_conn,self.player_map,self.player2_conn,self.player2_map)
    


    def init_game_board(self,conn):
        flag=True
        while flag:
            conn.send(self.action["Init_Ship"])
            try:         
                ship_array=pickle.loads(conn.recv(1024))
                flag = False
                for i in ship_array:
                    print(type(i))

                    if i<=9 or i>100 or (i>9 and i%10==0):
                        print("fail")
                        flag=True
                        
                
            except:
                flag=True
                conn.send(self.action["Error"])
        return ship_array



            

    def in_game(self,sock,List,sock2,List2):
   
        print("\n \n",List,List2)
        while len(List)!=0 and len(List2)!=0:
            flag=False
            
            sock.send(self.action["Turn"])

            data=int(self.recv_data(sock))
           
            for i in List2:
                if data==i:
                    flag=True
                    self.action["Hit"].set_coordinate(data)
                    sock.send(pickle.dumps(self.action["Hit"]))
                    break
            if flag:
                print("\n list 2 is :",List2)
                List2.remove(data)
                if(len(List2)==0):
                    sock.send(self.action["Win"])
                    sock2.send(self.action["Lose"])
                    break
            else:
                self.action["Miss"].set_coordinate(data)
                sock.send(pickle.dumps(self.action["Miss"]))
            flag=False
            

                     
            sock2.send(self.action["Turn"])
            
            data=int(self.recv_data(sock2))
            for i in List:
                if data==i:
                    flag=True
                    self.action["Hit"].set_coordinate(data)
                    sock2.send(pickle.dumps(self.action["Hit"]))
                    break
            if flag:
                print(len(List))
                List.remove(data)
                if len(List)==0:
                    sock2.send(self.action["Win"])
                    sock.send(self.action["Lose"])
                    break
                
            else:
                self.action["Miss"].set_coordinate(data)
                sock2.send(pickle.dumps(self.action["Miss"]))

    def recv_data(self,sock):
        flag=True
        while flag:
            data=sock.recv(1024)
            if data:
                print(" \n the data is :",data)
                return data
                break  

a=Server()
