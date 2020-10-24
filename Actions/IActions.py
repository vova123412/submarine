
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

    def do_action(self,sock):
         print("Win")
         sock.close()



class Turn(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock):
        print("Turn")
        self.send_data(sock)

    def send_data(self,sock):
        flag_s=True
        while flag_s:
            x=int(input("11-99  => 1,1 -9,9"))
            if(x>9 and x<100):
                flag_s=False
        sock.send(str(x).encode('ascii'))
    

class Miss(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock):
         print("Miss")


class Lose(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock):
        print("Lose")
        sock.close()


class Hit(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock):
        print("hit")












class Init_Ship(IActions):
    def __init__(self):
        pass


    def do_action(self,sock):
        print("init your ships")
        self.send_List(sock)

    

    def send_List(self,sock):
        List=self.init_List()
        P_List=pickle.dumps(List)
        sock.send(P_List)
    


    def init_List(self):
        List=[]
        length=0
        while(length<2):
            x=int(input("place the ship "))
            if(self.inList(List,x)):
                length=length+1
                List.append(x)
            else:
                print("invalid number")
        return List


    def inList(self,List,value):
        for i in List:
            if i==value:
                return False
        return True
        

class Error(IActions):
    def __init__(self):
        pass
    def do_action(self,sock):
        print("error")