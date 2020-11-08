from tkinter import *
from .GameFrame import *
class SubmarinApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Welcome to LikeGeeks app")
        self.geometry('1980x1300')
        self.frame=GameFrame(self)
        self.frame.grid(row=0,column=0)
        self.showframe()
       
      
    def showframe(self):
        self.frame.tkraise()
        