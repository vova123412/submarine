
from abc import ABC, abstractmethod
import pickle
class IActions(ABC):
 
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def do_action(self):
        pass


class Win(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,matrix):
        print("Win")
        sock.close()
        return 0



class Turn(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,matrix):
        print("Turn")
        self.send_data(sock)
        return 10

    def send_data(self,sock):
        flag_s=True
        while flag_s:
            x=int(input("11-99  => 1,1 -9,9"))
            if(x>9 and x<100):
                flag_s=False
        sock.send(str(x).encode('ascii'))
    

class Miss(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,matrix):
        print("Miss")
        matrix[self.coordinate]=-1
        self.Print(matrix)


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)

    def Print(self,matrix):
        Lmatrix =[ matrix[i:i+10] for i in range(0,len(matrix),10) ]
        for i in Lmatrix:
            print(i)


class Lose(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,matrix):
        print("Lose")
        sock.close()
        return 0


class Hit(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,matrix):
        print("hit")
        matrix[self.coordinate]=1
        self.Print(matrix)
  


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)


    def Print(self,matrix):
        Lmatrix =[ matrix[i:i+10] for i in range(0,len(matrix),10) ]
        for i in Lmatrix:
            print(i)





#what data
class Send_Ship(IActions):
    def __init__(self):
        pass


    def do_action(self,sock,matrix):
        print("init your ships")
        self.send_List(sock)
        return 10

    

    def send_List(self,sock):
        List=self.Validate_ShipList()
        P_List=pickle.dumps(List)
        sock.send(P_List)
    


    def Validate_ShipList(self):
        shiplist=[]     #was List 
        length=0
        while(length<2):
            x=int(input("place the ship "))
            if(self.inShipList(shiplist,x)):
                length=length+1
                shiplist.append(x)
            else:
                print("invalid number")
        return shiplist


    def inShipList(self,List,value):  #was inList
        for i in List:
            if i==value:
                return False
        return True
        

class Error(IActions):
    def __init__(self):
        pass
    def do_action(self,sock):
        print("error")
        return 0