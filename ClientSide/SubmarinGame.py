         
import socket
import pickle
class SubmarinGame:
    def __init__(self,sock,frame):
        self.sock=sock
        self.frame=frame
        


    def Actions_loop(self):
        while True:
            action_strategy=pickle.loads(self.sock.recv(1024))     # recv what?   action
            if action_strategy.do_action(self.sock,self.frame)==0:
                break
        print("SubmarinGame Over")

