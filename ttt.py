from tictactoe.board import Board
from tictactoe.players import ConsolePlayer, AIPlayer
from tictactoe.outputs import ConsoleOutput
from tictactoe.game import Game

number_of_players = int(raw_input('How many players? '))
if number_of_players == 1:
    play_as_player = int(raw_input('Play as player? '))
else:
    play_as_player = None


player1 = AIPlayer(mark='x') if number_of_players == 0 or (number_of_players == 1 and play_as_player == 2) else ConsolePlayer(mark='x')
player2 = AIPlayer(mark='o') if number_of_players == 0 or (number_of_players == 1 and play_as_player == 1) else ConsolePlayer(mark='o')
board = Board(3)
game = Game(player1, player2, board)
output = ConsoleOutput()
game.observer = output
game.start()