from random import randint
from threading import Thread, Lock
from Actions.IActions import *
import os
import socket
import json
import pickle
import time
import sys
import time
class Server():
    def __init__(self):
        self.users=[]
        self.threads=[]
        self.semaphore =True
        HOST = ''  
        PORT = 65432       
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        matches= Thread(target=self.match)
        self.threads.append(matches)
        matches.start()
        player_idx=0
        while player_idx<5: 
            conn, addr = sock.accept()
            print('Connected by', addr)
            user={
                'status':0,
                'index':player_idx,
                'addr':addr,
                'sock':conn,
                }
            player_idx=player_idx+1
            self.users.append(user)
            t = Thread(target=self.play,args=(conn,user))
            self.threads.append(t)
            t.start()
        self.semaphore =False
        sys.exit() 




    def match(self):
        while self.semaphore :
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
    
    def statusendgame(self,player_one_idx,player_two_idx):
        self.users[player_one_idx]['status']=0
        self.users[player_two_idx]['status']=0

    def create_new_game(self,player_one_idx,player_two_idx):
        one_vs_one=Game(self.users[player_one_idx]['sock'],self.users[player_two_idx]['sock'],player_one_idx,player_two_idx,self)
        

    def searchforgames(self):
        while self.semaphore :
            players_idx=[]
            for i in self.users:
                if i['status']==1:
                    players_idx.append(i['index'])
                if len(players_idx)==2:
                    print("match found")
                    return players_idx


                
                   
        


    def play(self,conn,user):
        while self.semaphore :
            if self.users[user['index']]['status']!=2 and self.users[user['index']]['status']!=1:
                message=pickle.dumps(Options())
                conn.send(message)
                data= self.recv_data(conn)
                print(data)
                if data=="search":
                    conn.send(pickle.dumps(Wait()))
                    self.searchgamestatus(user)
                    print(self.users[user['index']]['status'])
                    time.sleep(3)


                    
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
    def  __init__(self,player_conn,player2_conn,player_idx,player2_idx,server):
        self.player_idx=player_idx
        self.player2_idx=player2_idx
        self.server=server
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
        "Error":pickle.dumps(Error()),
        "HitMe":HitMe()
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
                    self.action["HitMe"].set_coordinate(data)
                    sock.send(pickle.dumps(self.action["Hit"]))
                    sock2.send(pickle.dumps(self.action["HitMe"]))
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
                self.action["HitMe"].set_coordinate(data)
                sock.send(pickle.dumps(self.action["Miss"]))
                sock2.send(pickle.dumps(self.action["HitMe"]))
            flag=False
            

                     
            sock2.send(self.action["Turn"])
            
            data=int(self.recv_data(sock2))
            for i in List:
                if data==i:
                    flag=True
                    self.action["HitMe"].set_coordinate(data)
                    self.action["Hit"].set_coordinate(data)
                    sock2.send(pickle.dumps(self.action["Hit"]))
                    sock.send(pickle.dumps(self.action["HitMe"]))
                    break
            if flag:
                print(len(List))
                List.remove(data)
                if len(List)==0:
                    sock2.send(self.action["Win"])
                    sock.send(self.action["Lose"])
                    break
                
            else:
                self.action["HitMe"].set_coordinate(data)
                self.action["Miss"].set_coordinate(data)
                sock2.send(pickle.dumps(self.action["Miss"]))
                sock.send(pickle.dumps(self.action["HitMe"]))
        self.endgame()
    

    def endgame(self):
        print("we end here")
        self.server.statusendgame(self.player_idx,self.player2_idx)

    def recv_data(self,sock):
        flag=True
        while flag:
            data=sock.recv(1024)
            if data:
                print(" \n the data is :",data)
                return data
                break  

a=Server()
