
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

    def do_action(self,sock,gui):
        for i in range(len(gui.buttons)):
            gui.buttons[i].configure(bg="gray")
        
        print("Win")
        sock.close()
        return 0



class Turn(IActions):
 
    def __init__(self,):
        self.flag=True

    def do_action(self,sock,gui):
        print("attak its your turn ")
        for i in range(len(gui.buttons)):
            gui.buttons[i].configure(command= lambda i=i:self.send_attak(sock,i+11))
        return 10

    def send_attak(self,sock,coordiante):
        if(int(coordiante)>9 and int(coordiante)<100 and self.flag):
            self.flag=False
            print(coordiante)
            sock.send(str(coordiante).encode('ascii'))
    

class Miss(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,gui):
        print("Miss")
        print(self.coordinate-11)
        gui.buttons[self.coordinate-11].configure(bg="blue")


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)


class Lose(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,gui):
        for i in range(len(gui.buttons)):
            gui.buttons[i].configure(bg="gray")
        print("Lose")
        sock.close()
        return 0


class Hit(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,gui):
        print("hit")
        print(self.coordinate-11)
        gui.buttons[self.coordinate-11].configure(bg="red")
  


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)






class Init_Ship(IActions):
    def __init__(self):
        self.shiplist=[]


    def do_action(self,sock,gui):
        print("init your ships")
        for i in range(len(gui.buttons)):
            gui.buttons[i].configure(command= lambda i=i:self.init_Shiplist(sock,i+11,gui))
        return 10

    

    def send_Shiplist(self,sock):
        Pshiplist=pickle.dumps(self.shiplist)
        sock.send(Pshiplist)
    
    

    def init_Shiplist(self,sock,coordinate,gui):
        if(len(self.shiplist)<2):
            if(self.inList(int(coordinate))):
                self.shiplist.append(int(coordinate))
                print(coordinate)
                
                gui.buttons[coordinate-11].configure(bg="green")
                if(len(self.shiplist)==2):
                    print("send my ships")
                    self.send_Shiplist(sock)
                
            else:
                print("invalid number")

  



    def inList(self,value):
        for i in self.shiplist:
            if i==value:
                return False
        return True
        

class Error(IActions):
    def __init__(self):
        pass
    def do_action(self,sock):
        print("error")
        return 0