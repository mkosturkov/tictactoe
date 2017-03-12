

class Player:
    
    def __init__(self, **kargs):
        self.mark = kargs['mark']
        
    def make_move(self, board):
        pass
    
class ConsolePlayer(Player):
    
    def make_move(self, board):
        xy = raw_input('Player %s, Enter a move (xy): ' % self.mark)
        x, y = int(xy[0]), int(xy[1])
        board.mark_position(x, y, self)