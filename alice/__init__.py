
from hexgame import AbstractPlayer, HORIZ, VERTI, EMPTY
import random

class Player (AbstractPlayer):

    name = 'Alice'

    def play(self, board, direction, **options):

        cols = len(board)
        rows = len(board[0])
        x = random.randrange(cols)
        y = random.randrange(rows)

        while board[x][y] != EMPTY:
            x = random.randrange(cols)
            y = random.randrange(rows)

        return (x, y)
