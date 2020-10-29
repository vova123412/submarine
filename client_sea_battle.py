import socket
import pickle
import time
import threading

class One_Player:
    instance=None
    class __Player:
        def __init__(self):
            self.value=""
            self.flag=True
            self.matrix= [0] * 100
            self.threads=[]
            self.P_List="";
            HOST = '127.0.0.1' 
            PORT = 65432        
            self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.t = threading.Thread(target=self.recv,args=(self.sock,))
            self.threads.append(t)
            t.start()
            time.Sleep(2000)


        def Send_Data(self):
            flag_s=True
            while flag_s:
                x=input("11-99  => 1,1 -9,9")
                if(x>9 and x<100):
                    flag_s=False
                self.sock.send(str(x.encode('ascii')))
            return x

        def Init_Matrix(self):
            for i in range(9):
                self.matrix[i+1]=i+1
            for i in range(9):
                self.matrix[(i+1)*10]=i+1
        def Recv(self):
            flag=True
            data=None
            while flag:
                data=self.sock.recv(1024)
                if data:
                    flag= False
            return data
                
        def Get_Action(self,action):
            location=0
            while self.flag:
                data=action
                data=data.decode('ascii')
                data=str(data)
                if data:
                    print("\n",data)
                if data=="give me your ships":
                    send_List(sock)
                if data=="your turn":
                    location=send_data(sock)
                if data == "hit":
                    matrix[location]=1
                    p_matrix = [ matrix[i:i+10] for i in range(0,len(matrix),10) ]
                    for i in p_matrix:
                        print(i)
                if data=="miss":
                    matrix[location]=-1
                    p_matrix = [ matrix[i:i+10] for i in range(0,len(matrix),10) ]
                    for i in p_matrix:
                        print(i)
                if data=="win" or data=="lose":
                    sock.close()
                    self.flag=False
               

        def inList(self,List,value):
            for i in List:
                if i==value:
                    return False
            return True
            
                
        def init_List():
            List=[]
            length=0
            while(length<2):
                x=input("place the ship ")
                if(inList(List,x)):
                    length=length+1
                    List.append(x)
                else:
                    print("invalid number")
            return List
                

        def Send_List(self,sock):
            List=init_List()
            P_List=pickle.dumps(List)
            sock.send(P_List)
            
        def Print(self):
            print(self.value)


            
        def Set_Value(self,value):
            self.value=value
            

    def __new__(cls):
        if not One_Player.instance:
            instance=One_Player.__Player
        return instance
    
    def __getattr__(self,name):
        return (self.instance,name)
    def __setattr__(self, name):
        return setattr(self.instance,name)


def main():
    player=One_Player()
    player.recv(player)
    

main()
