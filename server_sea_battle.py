from random import randint
import os
import socket
import json
from threading import Thread, Lock
import pickle
import time
from Actions.IActions import *

# what is this proxy for?
# please revisit proxy pattern 
# maybe you could use a validator layer like decorator

    
    # this function is over 10 lines of code        

# Game Facade, but what game are we playing?
class FacadeSubmarinGame:
    def __init__(player_one_sock,player_two_sock,player_one_idx,player_two_idx,prematch):
        self.prematch=prematch
        self.player_idx=player_idx
        self.player2_idx=player2_idx
        self.server=server
        self.player_conn=player_conn
        self.player_map=[]
        self.player2_conn=player2_conn
        self.player2_map=[]
        self.action={
        "Send_Ship":pickle.dumps(Send_Ship()),
        "Turn":pickle.dumps(Turn()),
        "Miss":Miss(),
        "Hit":Hit(),
        "Win":pickle.dumps(Win()),
        "Lose":pickle.dumps(Lose()),
        "Error":pickle.dumps(Error()),
        }
        self.player_map= self.init_game_board(self.player_conn)
        self.player2_map=self.init_game_board(self.player2_conn)
        self.in_game(self.player_conn,self.player_map,self.player2_conn,self.player2_map) 




    def init_game_board(self,conn):
        conn.send(self.action["Send_Ship"])
        ship_array=pickle.loads(conn.recv(1024))
        while validate_game_board(ship_array):
            conn.send(self.action["Send_Ship"])
            ship_array=pickle.loads(conn.recv(1024))


    def validate_game_board(self,ship_array):
        try:         
            for i in ship_array:
                if i<=9 or i>100 or (i>9 and i%10==0):
                    print("fail")
                    return False
            return True
        except:
                conn.send(self.action["Error"])
        return False



    # using connection objects is not hiding 3d-party code like sockets -> moved to IAction


   
       
  
        
       
    # the function doesnt contain a verb
    def endinggamestatus(self,index,index2):
        self.prematch.changestatusendgame(index,index2)

        


    # this function is over 10 lines of code
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
        self.endinggamestatus()

    def recv_data(self,sock):
        while True:
            data=sock.recv(1024).decode("ascii")
            if data:
                print(" \n the data is :",data)
                return data
                break  





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


    # function name should contain a verb
    def changestatusingame(self,player_one_idx,player_two_idx):
        self.users[player_one_idx]['status']=2
        self.users[player_two_idx]['status']=2

     # function name should contain a verb
    def changestatusendgame(self,player_one_idx,player_two_idx):
        self.users[player_one_idx]['status']=0
        self.users[player_two_idx]['status']=0

    def create_new_game(self,player_one_idx,player_two_idx):
        one_vs_one=FacadeSubmarinGame(self.users[player_one_idx]['sock'],self.users[player_two_idx]['sock'],player_one_idx,player_two_idx,self)
        

    def searchforgames(self):
        while self.semaphore :
            players_idx=[]
            for i in self.users:
                if i['status']==1:
                    players_idx.append(i['index'])
                if len(players_idx)==2:
                    print("match found")
                    return players_idx



class PlayerMannger:
    def __init__(self,users):
        self.users=users

    def play(self,conn,user):
        while self.semaphore :
            if self.users[user['index']]['status']!=2 and self.users[user['index']]['status']!=1:
                message=pickle.dumps(Options())
                conn.send(message)
                data= self.recv_data(conn)
                print(data)
                if data=="search":
                    conn.send(pickle.dumps(WaitForOpponent()))
                    self.searchgamestatus(user)
                    print(self.users[user['index']]['status']) 
                    time.sleep(3)

    # watch levels of abstractions in this code
    # decoding and encoding are low level abstraction
                    
    def recv_data(self,sock):
        while True:
            data=sock.recv(1024).decode("ascii")
            if data:
                print(" \n the data is :",data)
                return data
                break  


    def searchgamestatus(self,user):
        self.users[user['index']]['status']=1


# what server?
class SocketMannager:
    # the constructor is over 10 lines of code
    def __init__(self):
        self.users=[]
        self.threads=[]
        HOST = ''  
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
            self.threadplayermannger(conn)

        self.semaphore =False
        sys.exit() 
    
    def threadplayermannger(self,conn):
        t = Thread(target=self.playermannger.play,args=(conn,user))
        self.threads.append(t)
        t.start()





        

        

socketmannager=SocketMannager()
socketmannager.prematch.threadfindmatch()
socketmannager.acceptplayers()












