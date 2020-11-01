import socket
import pickle
import time
import threading

# What is One_Player?

    # this name is not informative
    # this is a GOD Class
    # you have to make some changes and divide your code!



class Gmae:
    def __init__(self,sock):
        self.matrix= [0] * 100
        self.sock=sock
        


    def Init_Matrix(self):
        for i in range(9):
            self.matrix[i+1]=i+1
        for i in range(9):
            self.matrix[(i+1)*10]=i+1
    
    def print_matrix(self):
        Lmatrix =[ self.matrix[i:i+10] for i in range(0,len(self.matrix),10) ]
        for i in Lmatrix:
            print(i)

    def Actions_loop(self):
        while True:
            action_strategy=pickle.loads(self.sock.recv(1024))     # recv what?   action
            if action_strategy.do_action(self.sock)==0:
                break
        print("Game Over")



        

class ConnectionMannger:
    def __init__(self):
        self.value=""
        self.flag=True# what is flag?
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mygame=Game(self.sock)
        self.threads=[]
        self.P_List=""
        HOST = '127.0.0.1' 
        PORT = 65432


    # What Data?   -> in IAction


    def Init_Connection(self):
        
        self.sock.connect((HOST, PORT))
        self.mygame.Init_Matrix()
        self.t = threading.Thread(target=self.mygame.Actions_loop,args=())
        self.threads.append(t)
        t.start()
        time.Sleep(2000)




    # the function called "Get..." but doesnt return anything
    # the function is a Command not query
    # the function is over 10 lines of code



    # what list? -> moved to IAction
    # what the purpose of value parameter?  moved to IAction: validation of ship_array
            

            # initializing doesnt call of an input   ->moved to IAction

            






def main():
    player=ConnectionMannger()
    player.Init_Connection()


    

main()
