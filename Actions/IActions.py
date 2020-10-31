
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
        for i in range(len(gui.board)):
            gui.board[i].configure(bg="gray")
            gui.enemyboard[i].configure(bg="gray")
        print("Win")



class Turn(IActions):
 
    def __init__(self,):
        self.flag=True

    def do_action(self,sock,gui):
        print("attak its your turn ")
        for i in range(len(gui.enemyboard)):
            gui.enemyboard[i].configure(command= lambda i=i:self.send_attak(sock,i+11))
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
        gui.enemyboard[self.coordinate-11].configure(bg="blue")


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)


class Lose(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,gui):
        for i in range(len(gui.board)):
            gui.board[i].configure(bg="gray")
            gui.enemyboard[i].configure(bg="gray")
        print("Lose")



class Hit(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,gui):
        print("hit")
        print(self.coordinate-11)
        gui.enemyboard[self.coordinate-11].configure(bg="red")
  


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)






class Init_Ship(IActions):
    def __init__(self):
        self.shiplist=[]


    def do_action(self,sock,gui):
        gui.search.configure(text="in game")
        print("init your ships")
        gui.search.configure(command=lambda: self.disablesearch)
        for i in range(len(gui.board)):
            gui.board[i].configure(command= lambda i=i:self.init_Shiplist(sock,i+11,gui))
        return 10

    
    def disablesearch(self):
        pass
    def send_Shiplist(self,sock):
        Pshiplist=pickle.dumps(self.shiplist)
        sock.send(Pshiplist)
    
    

    def init_Shiplist(self,sock,coordinate,gui):
        if(len(self.shiplist)<2):
            if(self.inList(int(coordinate))):
                self.shiplist.append(int(coordinate))
                print(coordinate)
                
                gui.board[coordinate-11].configure(bg="green")
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
        


class Wait(IActions):
    def __init__(self):
        pass
    def do_action(self,sock,gui):
        print("Wait")
        gui.search.configure(command=lambda: self.donothing())
        gui.search.configure(text="waiting")
    
    def donothing(self):
        pass

class Error(IActions):
    def __init__(self):
        pass
    def do_action(self,sock,gui):
        print("error")
        return 0

class Options(IActions):
    def __init__(self):
        pass
    def do_action(self,sock,gui):
        print("options")
        gui.search.configure(text="search")
        gui.search.configure(command=lambda: self.play_one_vs_one(sock))
    
    def play_one_vs_one(self,sock):
        sock.send("search".encode("ascii"))