from random import randint
import os
import socket
import json
import threading
import pickle
import time
users=[]
threads = []



# what is this proxy for?
# please revisit proxy pattern
# maybe you could use a validator layer like decorator
class Proxy:

    def __init__(self,conn,player,index):
        self.index=index
        self.player=player
        game=Game()
        self.conn=conn
        self.enemy_index
    
    # this function is over 10 lines of code
    def Validate_Board(self):
        flag=True
        while flag:
            mesg="give me your ships"
            self.conn.send(mesg.encode('ascii'));
            try:         
                ship_array =pickle.loads( self.conn.recv(1024))
                flag = False
                for i in ship_array:
                    print(i)
                    if i<=9 or i>100 or (i>9 and i%10==0):
                        print("fail")
                        flag=True
            except:
                mesg="error wrong type".encode('ascii')
                flag=True
                self.conn.send(mesg)
        return ship_array

    # this function is over 10 lines of code
    def Validate_Coordinat(self,enemy_conn):
        # watch levels of abstractions in this code
        player_board=users[self.enemy_index]['List']
        enemy_board= users[self.enemy_index]['List']
        flag_s=True
        coordinate
        while flag_s:
            # decoding and encoding are low level abstraction
            coordinate=(int)(self.conn.recv(1024).decode('ascii'))
            if(coordinate>9 and coordinate<100):
                if(self.game.Attak(coordinate,enemy_board)):
                   enemy_board.Remove(coordinate)
                   if self.game.Win(enemy_board):
                        mesg="win".encode("ascii")
                        conn.send(mesg)
                   else:
                        mesg="hit".encode("ascii")
                        conn.send(mesg)
            coordinate=(int)(enemy_conn.recv(1024).decode('ascii'))
            if(coordinate>9 and coordinate<100):
                if(self.game.Attak(coordinate,player_board)):
                   player_board.Remove(coordinate)
                   if self.game.Win(player_board):
                        mesg="win".encode("ascii")
                        enemy_conn.send(mesg)
                   else:
                        mesg="hit".encode("ascii")
                        enemy_conn.send(mesg)
                    
            
        sock.send(str(x.encode('ascii')))
        return x

        print("validate coordinates")

        
    def Start():
        self.game.Init_Game_Board(self.Validate_Board())
        self.enemy_index=self.game.Wait(index,conn)
        self.game.Status_In_Game(index,enemy_index)
        self.game.in_game(users[index]['sock'],users[index]['List'],users[self.enemy_index]['sock'],users[self.enemy_index]['List'])
        self.game.Status_Ready(index)
        self.game.Status_Ready(enemy_index)

    def Close_Game(self,index,index2):
        users[index]['sock'].close()
        users[index2]['sock'].close()


    def recv_data(self,sock):
        flag=True
        while flag:
            data=sock.recv(1024)
            if data:
                print(" \n the data is :",data)
                return data
                break

        
        

# Game Facade, but what game are we playing?
class Game:
    global Users
    def __init__():
        self.string="asds"

    def Init_Game_Board(self,player_board,user):
        print("init boad")
        users[user['index']]['List']=player_board

    
    # function name should contain a verb
    def Status_Ready(self,user):
        for i in users[user['index']]['List']:
            print(i)
        users[user['index']]['status']=1;
        print("the status is" ,users[user['index']]['status'])
        print("the index is" ,users[user['index']]['index'])
        print("nice job")
    

    # using connection objects is not hiding 3d-party code like sockets
    def play(self,conn,user):
        global users
        self.wait(user['index'],conn)
        conn.close()

    # wait for what?
    def Wait(self,index,sock):
        global users
        index2=0
        flag=True # what is flag?
        while flag:
            for i in users:
                if i['status']==1 and i['index']!=index:
                    flag=False
                    index2=i['index']
        print("connected two players")
        self.Status_In_Game(index,index2)
        return index2
        
       
    # the function doesnt contain a verb
    def Status_In_Game(self,index,index2):
        global users
        users[index]['status']=2
        users[index2]['status']=2

        
    def Player_One_Game(self,coordinate,board):
        pass

    def Win(self,board):
        if len(board)==0:
            return True
        return False
    
    # command query seperation is violated!
    # this function is not making any changes
    def Attak(sekf,coordinate,board):
        for pos in board:
            if pos==coordinate:
                return True
        return False
    
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

        


        


# what server?
class Server:
    # the constructor is over 10 lines of code
    def __init__(self):
        global users
        global threads
     

        HOST = '127.0.0.1' 
        PORT = 65432        
        # the names are not good you didn't think about them at all
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
            proxy=Proxy(conn,user)
            t = threading.Thread(target=proxy.Start,args=())
            threads.append(t)
            t.start()




        

        

a=Server()
