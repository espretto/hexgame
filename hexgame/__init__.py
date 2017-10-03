
import random

VERTICAL = -1
HORIZONTAL = 1

class AbstractPlayer (object):

    def play (self, board, direction, **options):
        raise NotImplementedError()


class Game (object):

    def __init__ (self, cols=11, rows=11):
        self.board = [[0 for col in range(cols)] for row in range(rows)]

    def play (self, alice, bob):
          
        

        if random.random() > 0.5:
            alice.play(self.board, VERTICAL)
            bob.play(self.board, HORIZONTAL)
        else:
            bob.play(self.board, VERTICAL)
            alice.play(self.board, HORIZONTAL)
