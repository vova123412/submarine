from tkinter import *
from .Ship import *
class ShipBuilder():
    def __init__(self,frame):
        self.frame=frame
        self.image1 = PhotoImage(file="tenor.gif")
    @staticmethod
    def buildship(size,frame,image1):
        if size=="small":
            return Ship(frame,width=5,height=5,image=image1)
        elif size=="middle":
            return Ship(frame,width=10,height=5,image=image1)
        elif size=="large":
            return Ship(frame,width=15,height=5,image=image1)