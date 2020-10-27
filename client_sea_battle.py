import socket
import pickle
import time
import threading
from Actions.IActions import *
try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(background='skyblue')
        self.geometry('1000x700+250+50')
        self.resizable(width = False, height = False)
        self.title_font = tkfont.Font()
        container = tk.Frame(self)
        container.pack(side="top")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frames = {}
        for F in (Menu, MultiPlayer, SinglePlayer):
            page_name = F.__name__  
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            

        self.show_frame("Menu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()  #######################


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.configure(background='goldenrod4')
        self.controller = controller
        image1 = tk.PhotoImage(file="image.png")

        panel1 = tk.Label(self, image=image1)
        panel1.pack()
        panel1.image = image1

        
        label = tk.Label(self,font=controller.title_font)
        label.pack()
        button1 = tk.Button(self,width=100,pady=10, text="MultiPlayer",bg="red",command=lambda: controller.show_frame("MultiPlayer"))
        button2 = tk.Button(self,width=100,pady=10, text="SinglePlayer", command=lambda: controller.show_frame("SinglePlayer"))
        button1.pack(pady=10)
        button2.pack(pady=10)
      


class MultiPlayer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.labels=[]
        self.buttons=[]
        self.controller = controller
        self.client=Client(self)
        idx=[]
        menu = tk.Button(self, text="Go to the menu",command=lambda: controller.show_frame("Menu"))
        menu.grid(row=25,column=20)
       
        for i in range(0,10):
            self.labels.append(tk.Label(self,text=str(i),padx=10))
            self.labels[i].grid(row=0,column=int(i%10))
            
        for i in range(1,10):
            self.labels.append(tk.Label(self,text=str(i),pady=10))                   
            self.labels[i+9].grid(row=int(i%10),column=0)
            
        for i in range(89):
            idx.append(i)
            self.buttons.append(tk.Button(self,text=str(i+11),width=4))
            y=int(i/10+1)
            x=int(i%10+1)
            print(x)
            if x!=10:
                self.buttons[i].grid(row=y,column=x)
        
        search=tk.Button(self,text="search for game",command= lambda: self.searchGame())
        search.grid(row=20,column=20)


    def searchGame(self):
        self.client.init_conn()


class SinglePlayer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the menu",command=lambda: controller.show_frame("Menu"))
        button.pack()




class Client():
    def __init__(self,gui):
        self.gui=gui

    def changecolor(self):
        self.gui.buttons[1].configure(bg="green")
            
    def play(self,sock):
        while True:
            action_strategy=pickle.loads(sock.recv(1024))
            if action_strategy.do_action(sock,self.gui)==0:
                break
        print("Game Over")


    def init_conn(self):
        threads=[]
        P_List=""
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 65432        # The port used by the server
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        t = threading.Thread(target=self.play,args=(sock,))
        threads.append(t)
        t.start()

   

app = SampleApp()
app.mainloop()
