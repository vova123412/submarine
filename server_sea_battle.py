from random import randint
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
        #Settings Variables
        self.row_size = 9 #number of rows
        self.col_size = 9 #number of columns
        self.num_turns = 40
        #Create lists
        self.ship_list = []
        self.board = [self.row_size*self.col_size]
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(5)
        index=0
        flag=True
        while index<4: 
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

#Functions
    def print_board(self,board_array):
        pass






# Create the ships

    def init_game_board(self,conn):
        flag=True
        while flag:
            conn.send("give me your ships");
            try:         
                ship_array =pickle.loads( conn.recv(1024))
                flag = False
                for i in ship_array:
                    print(i)
                    if i<=9 or i>100 or (i>9 and i%10==0):
                        print("fail")
                        flag=True
                        
                
            except:
                flag=True
                conn.send("noob error wrong type")
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
            sock.send("your turn")
            data=int(self.recv_data(sock))
            for i in List2:
                if data==i:
                    flag=True
                    sock.send("hit")
                    break
            if flag:
                print("\n list 2 is :",List2)
                List2.remove(data)
                if(len(List2)==0):
                    time.sleep(4)
                    sock.send("win")
                    sock2.send("lose")
                    time.sleep(4)
                    break
            else:
                sock.send("miss")
            flag=False
            

            
            sock2.send("your turn")
            
            data=int(self.recv_data(sock2))
            for i in List:
                if data==i:
                    flag=True
                    sock2.send("hit")
                    break
            if flag:
                print(len(List))
                List.remove(data)
                if len(List)==0:
                    time.sleep(4)
                    sock2.send("win")
                    sock.send("lose")
                    time.sleep(4)
                    break
                
            else:
                sock2.send("miss")

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
        users[user['index']]['status']=1;
        print("the status is" ,users[user['index']]['status'])
        print("the index is" ,users[user['index']]['index'])
        print("nice job")
        self.wait(user['index'],conn)
        
        conn.close()
        

a=Server()
