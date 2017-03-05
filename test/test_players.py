import unittest
from tictactoe import players

class TestPlayers(unittest.TestCase):
    
    def test_player_mark(self):
        player = players.Player(mark='x')
        self.assertEquals('x', player.mark)