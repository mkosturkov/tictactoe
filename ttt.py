from tictactoe.board import Board
from tictactoe.players import ConsolePlayer
from tictactoe.outputs import ConsoleOutput
from tictactoe.game import Game

player1 = ConsolePlayer(mark='x')
player2 = ConsolePlayer(mark='o')
board = Board(3)
game = Game(player1, player2, board)
output = ConsoleOutput()
game.observer = output
game.start()