
from tkinter import *


class Ship(Label):
    def __init__(self,frame,width,height,image):
        self.x=50
        self.y=50
        self.minwidth=5
        self.minheitght=5
        self.width=width
        self.height=height
        self.ship=Label(frame,width=width,height=height,bg="green")
        self.ship.grid(row=1,column=1)
        self.make_draggable(self.ship)



    def stopdrag(self):
        self.ship.unbind("<Button-1>")
        self.ship.unbind("<B1-Motion>")


    def getcoordinate(self):

        if self.width>=self.height:
            return self.validatewidthcoordinate()
        else:
            return self.validateheightcoordinate()

    def validatewidthcoordinate(self):
        coordinate=[]
        width=self.width
        while width>0:
            if(int((self.x/50+width/self.minwidth-1))*10+int(self.y/50)<100 and int(self.y/50)>0 and int(self.x/50)>0):
               coordinate.append(int((self.x/50+width/self.minwidth-1))*10+int(self.y/50))
            width=width-self.minwidth
        return coordinate
        
    
    def validateheightcoordinate(self):
        coordinate=[]
        height=self.height
        while height>0:
            if(int(self.x/5)+int(self.y/50+height/self.minheight)<100):
                coordinate.append(int(self.x/5)+int(self.y/50+height/self.minheight-1) and int(self.y/50)>0 and int(self.x/50))
            heiht=height-self.minheight
        return coordinate
    
    def make_draggable(self,widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self,event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(self,event):
        widget = event.widget
        self.x = widget.winfo_x() - widget._drag_start_x + event.x
        self.y = widget.winfo_y() - widget._drag_start_y + event.y    
    
        if self.x<=(460-(self.width/self.minwidth-1)*50) and int(self.x/50)>0 and self.y<=(460-(self.height/self.minheitght-1)*50) and int(self.y/50)>0:


            print(f'x {self.x/50:} y: {self.y/50:}')
            shiplist=self.getcoordinate()
            for i in shiplist:
                print(i)
            widget.place(x=int(self.x),y=int(self.y))


            