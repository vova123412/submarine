from random import randint
from threading import Thread, Lock
from Actions.IActions import *
import os
import socket
import json
import pickle
import time
class Server():
    def __init__(self):
        self.users=[]
        self.threads=[]

        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(5)
        index=0
        flag=True
        while index<3: 
            conn, addr = sock.accept()
            print('Connected by', addr)
            user={
                'status':0,
                'index':index,
                'addr':addr,
                'sock':conn,
                'List':[]
                }
            index=index+1
            self.users.append(user)
            t = Thread(target=self.play,args=(conn,addr,user))
            self.threads.append(t)
            t.start()






    def play(self,conn,addr,user):
        self.users[user['index']]['status']=1
        print("the status is" ,self.users[user['index']]['status'])
        print("the index is" ,self.users[user['index']]['index'])
        print("nice job")
        self.wait(user['index'],conn)

    def wait(self,index,sock):
        mutex = Lock()
        index2=0
        flag=True
        mutex.acquire()
        try:
            while flag and self.users[index]['status']!=2:
                for i in self.users:
                    if i['status']==1 and i['index']!=index:
                        flag=False
                        index2=i['index']
                        self.users[index]['status']=2
                        self.users[index2]['status']=2
                        one_vs_one=Game(self.users[index]['sock'],self.users[index]['List'],self.users[index2]['sock'],self.users[index2]['List'])
            print("connected two players")

        finally:
            mutex.release()
        
        print("the mutch found")

    



class Game():
    def  __init__(self,player_conn,player_map,player2_conn,player2_map):
        self.player_conn=player_conn
        self.player_map=player_map
        self.player2_conn=player2_conn
        self.player2_map=player2_map
        self.action={
        "Init_Ship":pickle.dumps(Init_Ship()),
        "Turn":pickle.dumps(Turn()),
        "Miss":pickle.dumps(Miss()),
        "Hit":pickle.dumps(Hit()),
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
                   
                    sock.send(self.action["Hit"])
                    break
            if flag:
                print("\n list 2 is :",List2)
                List2.remove(data)
                if(len(List2)==0):
                    sock.send(self.action["Win"])
                    sock2.send(self.action["Lose"])
                    break
            else:
                
                sock.send(self.action["Miss"])
            flag=False
            

                     
            sock2.send(self.action["Turn"])
            
            data=int(self.recv_data(sock2))
            for i in List:
                if data==i:
                    flag=True
                    sock2.send(self.action["Hit"])
                    break
            if flag:
                print(len(List))
                List.remove(data)
                if len(List)==0:
                    sock2.send(self.action["Win"])
                    sock.send(self.action["Lose"])
                    break
                
            else:
                sock2.send(self.action["Miss"])

    def recv_data(self,sock):
        flag=True
        while flag:
            data=sock.recv(1024)
            if data:
                print(" \n the data is :",data)
                return data
                break  

a=Server()
