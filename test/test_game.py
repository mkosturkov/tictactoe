import unittest

import tictactoe
from tictactoe import game

class TestGame(unittest.TestCase):
    
    board_size = 3
    p1_mark = 'x'
    p2_mark = 'o'
    
    def setUp(self):
        self.p1 = tictactoe.players.Player(mark=self.p1_mark)
        self.p2 = tictactoe.players.Player(mark=self.p2_mark)
        self.board = tictactoe.board.Board(self.board_size)
        self.game = tictactoe.game.Game(self.p1, self.p2, self.board)
        
    def test_game_loop(self):
        test_case = self
        player1_moves_count = [0]
        player2_moves_count = [0]
        
        def player1_make_move(board):
            board.mark_position(player1_moves_count[0], 0, test_case.p1)
            player1_moves_count[0] += 1
            
        def player2_make_move(board):
            board.mark_position(player2_moves_count[0], 1, test_case.p2)
            player2_moves_count[0] += 1
            
        class ObserverClass:
            
            def __init__(self):
                self.times_observed = 0
                self.state_checks = []
                self.expected_states = [
                    [
                        [None, None, None],
                        [None, None, None],
                        [None, None, None]
                    ],
                    [
                        [test_case.p1, None, None],
                        [None, None, None],
                        [None, None, None]
                    ],
                    [
                        [test_case.p1, None, None],
                        [test_case.p2, None, None],
                        [None, None, None]
                    ],
                    [
                        [test_case.p1, test_case.p1, None],
                        [test_case.p2, None, None],
                        [None, None, None]
                    ],
                    [
                        [test_case.p1, test_case.p1, None],
                        [test_case.p2, test_case.p2, None],
                        [None, None, None]
                    ],
                    [
                        [test_case.p1, test_case.p1, test_case.p1],
                        [test_case.p2, test_case.p2, None],
                        [None, None, None]
                    ],
                ]
            
            def observe(self, game):
                state = self.get_state(game.board)
                test_case.assertEquals(self.expected_states[self.times_observed], state)
                self.times_observed += 1
                
            def get_state(self, board):
                state = []
                for y in range(test_case.board_size):
                    state.append([])
                    for x in range(test_case.board_size):
                        state[y].append(board.positions[y][x].get_marked_player())
                return state
        
        self.p1.make_move = player1_make_move
        self.p2.make_move = player2_make_move
        observer = ObserverClass()
        self.game.observer = observer
        self.game.start()
        
        self.assertEquals(len(observer.expected_states), observer.times_observed)
        self.assertTrue(self.game.is_won())
        self.assertEquals(self.p1, self.game.winner)
        
    def test_no_winner(self):
        state = [
            [self.p2, self.p1, self.p2],
            [self.p2, self.p1, self.p2],
            [self.p1, self.p2, None]
        ]
        for y in range(self.board_size):
            for x in range(self.board_size):
                self.board.mark_position(x, y, state[y][x])
        
        self.p1.make_move = lambda board: board.mark_position(2, 2, self.p1)
        class ObserverClass:
            observed_times = 0
            
            def observe(self, game):
                self.observed_times += 1
                
        observer = ObserverClass()
        self.game.observer = observer
        self.game.start()
        
        self.assertEquals(2, observer.observed_times)
        self.assertFalse(self.game.is_won())