import unittest

import tictactoe
from tictactoe import board
from tictactoe import players
from tictactoe import ai


class TestAI(unittest.TestCase):
    
    board_size = 3
    
    def setUp(self):
        self.p1 = players.Player(mark='x')
        self.p2 = players.Player(mark='o')
        self.board = board.Board(self.board_size)
        
    def test_compare_score_positions_owned(self):
        self._test_two_way_comparison(ai.Score(2, 2, 'x'), ai.Score(1, 2, 'y'))
        
    def test_compare_score_number_of_combinations(self):
        self._test_two_way_comparison(ai.Score(2, 2, 'x'), ai.Score(2, 1, 'y'))
        
    def test_compare_score_equal(self):
        self.assertEquals(0, ai.compare_scores(ai.Score(2, 2, 'x'), ai.Score(2, 2, 'y')))
        
    def test_bind_positions_to_lines(self):
        positions_with_lines = ai.bind_positions_to_lines([self.board.positions[0][0], self.board.positions[1][1]], self.board)
        self.assertEquals(3, len(positions_with_lines[0]['lines']))
        self.assertEquals(4, len(positions_with_lines[1]['lines']))
        for p in positions_with_lines:
            for line in p['lines']:
                self.assertIn(p['position'], line.positions)
        
    def test_get_unmarked_positions(self):
        self._set_state_from_filled_positions(((0, 0, self.p1), (2, 2, self.p1)))
        unmarked_positions = ai.get_unmarked_positions(self.board)
        self.assertEquals(self.board_size ** 2 - 2, len(unmarked_positions))
        self.assertNotIn(self.board.positions[0][0], unmarked_positions)
        self.assertNotIn(self.board.positions[2][2], unmarked_positions)
        
    def test_get_most_positions_owned_in_lines_count(self):
        pf = lambda p: p == self.p1
        self.assertEquals(0, ai.get_most_positions_owned_in_lines_count(pf, self.board.get_lines()))
        self._set_state_from_filled_positions([(0, 0, self.p1)])
        self.assertEquals(1, ai.get_most_positions_owned_in_lines_count(pf, self.board.get_lines()))
        self._set_state_from_filled_positions([(2, 0, self.p1), (1, 1, self.p1)])
        self.assertEquals(2, ai.get_most_positions_owned_in_lines_count(pf, self.board.get_lines()))
        
    def test_get_number_of_possible_combinations(self):
        pf = lambda p: p == self.p1
        lines = self.board.get_lines()
        self.assertEquals(len(lines), ai.get_number_of_possible_combinations(pf, lines))
        self._set_state_from_filled_positions([(1, 1, self.p2)])
        self.assertEquals(len(lines) - 4, ai.get_number_of_possible_combinations(pf, lines))
        self._set_state_from_filled_positions([(0, 0, self.p2)])
        self.assertEquals(len(lines) - 6, ai.get_number_of_possible_combinations(pf, lines))
        
    def test_get_single_score(self):
        pf = lambda p: p == self.p1
        lines = self.board.get_lines()
        score = ai.get_single_score(pf, {'position': self.board.positions[1][1], 'lines': lines})
        self.assertTrue(isinstance(score, ai.Score))
        self.assertEquals(len(lines), score.number_of_combinations)
        self.assertEquals(0, score.positions_owned)
        self.assertEquals(self.board.positions[1][1], score.position)
        
    def test_get_scores(self):
        self.assertEquals(self.board_size ** 2, len(ai.get_scores(lambda _: True, self.board)))
        self._set_state_from_filled_positions([(0, 0, self.p1)])
        self.assertEquals(self.board_size ** 2 - 1, len(ai.get_scores(lambda _: True, self.board)))
        
    def test_get_top_scores(self):
        input_scores = [ai.Score(2, 2, 'x'), ai.Score(2, 1, 'x'), ai.Score(2, 2, 'x')]
        top_scores = ai.get_top_scores(input_scores)
        self.assertEquals(2, len(top_scores))
        self.assertIn(top_scores[0], input_scores)
        self.assertIn(top_scores[1], input_scores)
        
    def test_first_move(self):
        scores = ai.get_best_moves_for_player(self.p1, self.board)
        self.assertEquals(1, len(scores))
        self.assertEquals(self.board.positions[1][1], scores[0].position)
        
    def test_second_move(self):
        self._set_state_from_filled_positions([(1, 1, self.p2)])
        scores = ai.get_best_moves_for_player(self.p1, self.board)
        self.assertEquals(4, len(scores))
        p = self.board.positions
        for score in scores:
            self.assertIn(score.position, [p[0][0], p[0][2], p[2][0], p[2][2]])
    
    def _test_two_way_comparison(self, score1, score2):
        self.assertLess(0, ai.compare_scores(score1, score2))
        self.assertGreater(0, ai.compare_scores(score2, score1))
    
    def _execute(self):
        return ai.get_best_moves_for_player(self.p1, self.board)
    
    def _set_state_from_filled_positions(self, positions):
        for x, y, player in positions:
            self.board.mark_position(x, y, player)
    
    def _set_state(self, state):
        for y in range(self.board_size):
            for x in range(self.board_size):
                self.board.mark_position(x, y, state[y][x])