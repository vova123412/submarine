from random import randint
from Actions.IActions import *
import os
import socket
import json
import threading
import pickle
import time
users=[]
threads = []
class Server:
    def __init__(self):
        global users
        global threads
        self.action={
        "Init_Ship":pickle.dumps(Init_Ship()),
        "Turn":pickle.dumps(Turn()),
        "Miss":pickle.dumps(Miss()),
        "Hit":pickle.dumps(Hit()),
        "Win":pickle.dumps(Win()),
        "Lose":pickle.dumps(Lose()),
        "Error":pickle.dumps(Error())
        }
        #Settings Variables
        #Create lists
        self.ship_list = []

        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(5)
        index=0
        flag=True
        while index<2: 
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
            users.append(user)
            t = threading.Thread(target=self.play,args=(conn,addr,user))
            threads.append(t)
            t.start()


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

    def recv_data(self,sock):
        flag=True
        while flag:
            data=sock.recv(1024)
            if data:
                print(" \n the data is :",data)
                return data
                break
            

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


    def wait(self,index,sock):
        global users
        index2=0
        flag=True
        while flag:
            for i in users:
                if i['status']==1 and i['index']!=index:
                    flag=False
                    index2=i['index']
        print("connected two players")
        users[index]['status']=2
        users[index2]['status']=2
        self.in_game(users[index]['sock'],users[index]['List'],users[index2]['sock'],users[index2]['List'])
        users[index]['sock'].close()
        users[index2]['sock'].close()

    def play(self,conn,addr,user):
        global users
        User_List=self.init_game_board(conn)
        users[user['index']]['List']=User_List
        print("user list")
        for i in users[user['index']]['List']:
            print(i)
        users[user['index']]['status']=1
        print("the status is" ,users[user['index']]['status'])
        print("the index is" ,users[user['index']]['index'])
        print("nice job")
        self.wait(user['index'],conn)
        

a=Server()
