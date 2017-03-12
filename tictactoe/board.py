

class Position:
    
    def __init__(self):
        self._player = None
        
    def is_marked(self):
        return self._player != None
    
    def mark_player(self, player):
        self._player = player
    
    def get_marked_player(self):
        return self._player
    
class Line:
    
    def __init__(self, positions):
        self.positions = positions
        
    def __len__(self):
        return len(self.positions)
    
    def wins(self):
        last_player = None
        for position in self.positions:
            if not position.is_marked() or (last_player is not None and position.get_marked_player() != last_player):
                return False
            last_player = position.get_marked_player()
        return True
    
    def get_player_at_position(self, position):
        return self.positions[position].get_marked_player()


class Board:
    
    def __init__(self, size):
        self._size = size
        self.positions = [[Position() for x in range(size)] for y in range(size)]
    
    def get_lines(self):
        lines = []
        diag1 = []
        diag2 = []
        for i in range(self._size):
            diag1.append(self.positions[i][i])
            diag2.append(self.positions[self._size - i - 1][i])
            horizontal = []
            vertical = []
            for j in range(self._size):
                horizontal.append(self.positions[i][j])
                vertical.append(self.positions[j][i])
            lines.append(Line(horizontal))
            lines.append(Line(vertical))
        lines.append(Line(diag1))
        lines.append(Line(diag2))
        return lines
    
    def mark_position(self, x, y, player):
        if self.positions[y][x].is_marked():
            raise Exception('Already marked')
        self.positions[y][x].mark_player(player)        
