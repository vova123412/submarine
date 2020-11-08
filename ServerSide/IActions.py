
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

    def do_action(self,sock,frame):
        print("Win")
        sock.close()
        return 0



class WaitForOpponent(IActions):

 
    def __init__(self,):
        pass

    def do_action(self,sock,frame):
        frame.startgame.configure(text="wait for opponent",command= lambda :self.donothing())
        
        print("wait for opponent")

    def donothing(self):
        pass

class Turn(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,frame):
        print("Turn")
        frame.startgame.config(text="attak")
        for i in range(0,100):
            if(int(i/10)!=0 and int(i%10)!=0):
                frame.labelsboard[i+100].bind("<1>",lambda e,i=i:self.send_coordinate(frame,sock,i))
        return 10

    def send_coordinate(self,frame,sock,coordinate):
        print("the coordinate is ",coordinate)
        sock.send(str(coordinate).encode('ascii'))
        for i in range(0,100):
            if(int(i/10)!=0 and int(i%10)!=0):
                frame.labelsboard[i+100].bind("<1>",lambda e,i=i:self.donothing())
    

    def donothing(self):
        pass
     

class Miss(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,frame):
        print("Miss")
        frame.labelsboard[self.coordinate+100].configure(text="miss",bg="white")
        frame.labelsboard[self.coordinate+100].tkraise()
        


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)



class Lose(IActions):
 
    def __init__(self,):
        pass

    def do_action(self,sock,frame):
        print("Lose")
        sock.close()
        return 0


class Hit(IActions):
 
    def __init__(self,):
        self.coordinate=11

    def do_action(self,sock,frame):
        print("hit")
        frame.labelsboard[self.coordinate+100].configure(text="hit",bg="red")
        frame.labelsboard[self.coordinate+100].tkraise()
  


    def set_coordinate(self,coordinate):
        self.coordinate=int(coordinate)






#what data
class Send_Ship(IActions):
    def __init__(self):
        pass


    def do_action(self,sock,frame):
        print("init your ships")
        frame.startgame.config(text="init board ",command= lambda: self.donothing())
        frame.sendcoordinate.configure(command= lambda :self.send_List(sock,frame))
        return 10

    def donothing(self):
        pass

    def send_List(self,sock,frame):
        shiplist=frame.getcoordinatelist()
        frame.unbindshipslist()
        pshiplist=pickle.dumps(shiplist)
        sock.send(pshiplist)
    



        

class Options(IActions):
    def __init__(self):
        pass
    def do_action(self,sock,frame):
        sock.send("search".encode("ascii"))

class Error(IActions):
    def __init__(self):
        pass
    def do_action(self,sock,frame):
        print("error")
        return 0