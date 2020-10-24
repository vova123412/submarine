from .IActions import IActions
class Hit(IActions):
 
    def __init__(self,game_matrix):
        self.matrix= game_matrix

    def do_action(self):
        Lmatrix =[ self.matrix[i:i+10] for i in range(0,len(self.matrix),10) ]
        for i in Lmatrix:
            print(i)
        print("\n hit")


    def set_miss_coordinate(self,coordinate):
        self.matrix[coordinate]=1

