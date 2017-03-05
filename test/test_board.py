import unittest

from tictactoe import players
from tictactoe import board


class TestPosition(unittest.TestCase):
    
    def setUp(self):
        self.position = board.Position()
    
    def test_mark(self):
        self.assertFalse(self.position.is_marked())
        self.position.mark_player('p1')
        self.assertTrue(self.position.is_marked())
        self.assertEquals('p1', self.position.get_marked_player())
        

class TestLine(unittest.TestCase):
    
    def setUp(self):
        self.positions_count = 3
        self.line = board.Line(self._make_positions(self.positions_count))
    
    def test_size(self):
        self.assertEquals(self.positions_count, len(self.line))
        
    def test_wins(self):
        self.assertFalse(self.line.wins())
        positions = self._make_positions(self.positions_count)
        for i in range(self.positions_count):
            positions[i].mark_player('x')
        line = board.Line(positions)
        self.assertTrue(line.wins())
        
    def test_get_player_at_position(self):
        player1, player2 = players.Player(mark='x'), players.Player(mark='y') 
        position1, position2 = board.Position(), board.Position()
        position1.mark_player(player1)
        position2.mark_player(player2)
        line = board.Line([position1, position2])
        self.assertEquals(player1, line.get_player_at_position(0))
        self.assertEquals(player2, line.get_player_at_position(1))
        
    @classmethod
    def _make_positions(cls, count):
        return tuple(board.Position() for i in range(count))



class TestBoard(unittest.TestCase):
    
    
    
    def setUp(self):
        self.dimension_size = 3
        self.board = board.Board(self.dimension_size)
    
    def test_lines_count(self):
        self.assertEquals(2 * self.dimension_size + 2, len(self.board.get_lines()))
        
    def test_mark_position(self):
        self.board.mark_position(1, 1, 'x')
        with self.assertRaises(Exception) as context:
            self.board.mark_position(1, 1, 'x')
        self.assertTrue(hasattr(context, 'exception'))
        
    def test_set_state(self):
        pass