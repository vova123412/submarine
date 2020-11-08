from tkinter import *
from .ConnectionMannger import *
from .ShipBuilder import *
class GameFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent,width=1000, height=1000)
        self.labelsboard=[]
        self.image1 = PhotoImage(file="tenor.gif")
        self.sendcoordinatebutton=None
        self.startgame=None
        self.shipslist=[]
        self.initbuttons()
        self.initboards()
        self.initships()
        self.player=ConnectionMannger(self)

        



    
    def initconnection(self):
        self.player.Init_Connection()
        self.player.Play()
    
    def initbuttons(self):
        self.sendcoordinatebutton=Button(self,width=20,pady=10, text="send ships",bg="red",command=lambda: self.getcoordinatelist())
        self.sendcoordinatebutton.grid(row=2,column=20)

        self.startgame=Button(self,width=20,pady=10, text="connect",bg="red",command=lambda: self.initconnection())
        self.startgame.grid(row=45,column=80)



    def initboards(self):
        for i in range(0,100):
            self.labelsboard.append(Label(self,text=str(i),padx=17,pady=17 ))
            self.labelsboard[i].grid(row=int(i/10),column=int(i%10))
        
        Label(self,text="Enemy board       =>",padx=17,pady=17).grid(row=5,column=20)
        Label(self,text="<=       your board dnd ship ",padx=17,pady=17).grid(row=4,column=20)

        for i in range(0,100):
            self.labelsboard.append(Label(self,text=str(i),padx=17,pady=17 ))
            self.labelsboard[i+100].grid(row=int(i/10),column=int(i%10)+50)


    def getcoordinatelist(self):
        coordinate=[]
        for ship in self.shipslist:
            for i in ship.getcoordinate():
                coordinate.append(i)
        return coordinate
       
    def unbindshipslist(self):
        for ship in self.shipslist:
            ship.stopdrag()


    def initships(self):
        self.shipslist.append(ShipBuilder.buildship("small",self,self.image1))
        self.shipslist.append(ShipBuilder.buildship("middle",self,self.image1))



        

