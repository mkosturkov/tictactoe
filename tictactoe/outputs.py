

class ConsoleOutput:
    
    def observe(self, game):
        print
        print
        
        if game.error:
            print game.error
            return
        
        for rows in game.board.positions:
            rowstr = ' |'
            for position in rows:
                rowstr += ' '
                if not position.is_marked():
                    rowstr += '_'
                else:
                    rowstr += position.get_marked_player().mark
                rowstr += ' |'
            print rowstr
        print
        print
        
        if game.is_won():
            print 'Winner is: ' + game.winner.mark
            print

            