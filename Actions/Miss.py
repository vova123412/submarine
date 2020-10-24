from .IActions import IActions,Stack
class Miss(IActions):
 
    def __init__(self,g):
        self.coordinate=0
    def do_action(self):
        print(" \n Miss")
    

    def set_miss_coordinate(self,coordinate):
        self.coordinate=coordinate





       


        
