from .IActions import IActions
class Hit(IActions):
 
    def __init__(self,game_matrix):
        self.matrix= game_matrix

    def do_action(self):
        print("\n hit")


