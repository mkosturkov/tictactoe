

class Game:
    
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.winner = None
        self.observer = None
        self.error = None
    
    def is_won(self):
        return self.winner != None
    
    def start(self):
        players = (self.player1, self.player2)
        current_player_index = 0
        self._observe()
        while True:
            current_player = players[current_player_index]
            try:
                current_player.make_move(self.board)
            except Exception, e:
                self.error = e.message
                self._observe()
                self.error = None
                continue
            self._set_winner()
            self._observe()
            if self._ended():
                break
            else:
                current_player_index ^= 1
                
    def _ended(self):
        if self.is_won():
            return True
        
        for row in self.board.positions:
            for position in row:
                if not position.is_marked():
                    return False
        return True
            
    def _set_winner(self):
        for line in self.board.get_lines():
            if line.wins():
                self.winner = line.get_player_at_position(0)
                return
    
    
    def _observe(self):
        if self.observer != None:
            self.observer.observe(self)
    
