import socket
import pickle
import time
import threading
flag=True
matrix= [0] * 100
for i in range(9):
    matrix[i+1]=i+1
for i in range(9):
    matrix[(i+1)*10]=i+1
    
def send_data(sock):
    flag_s=True
    while flag_s:
        x=input("11-99  => 1,1 -9,9")
        if(x>9 and x<100):
            flag_s=False
    sock.send(str(x))
    return x
        
def recv(sock):
    global flag
    location=0
    global matrix
    while flag:
        data=sock.recv(1024)
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
                print i
        if data=="miss":
            matrix[location]=-1
            p_matrix = [ matrix[i:i+10] for i in range(0,len(matrix),10) ]
            for i in p_matrix:
                print i
        if data=="win" or data=="lose":
            sock.close()
            flag=False
       

def inList(List,value):
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
        

def send_List(sock):
    List=init_List()
    P_List=pickle.dumps(List)
    sock.send(P_List)
    


def init_conn():
    global flag
    threads=[]
    P_List="";
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    t = threading.Thread(target=recv,args=(sock,))
    threads.append(t)
    t.start()
    

    
    time.sleep(200)
    flag=False

init_conn()
