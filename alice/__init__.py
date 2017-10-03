
from hexgame import AbstractPlayer, HORIZONTAL, VERTICAL
import random

class Player (AbstractPlayer):

    def play(self, board, direction, **options):
        print('Je suis ton adversaire, Alice')

        x = 1
        z = 2
        y = x+z

        return (x, y, z)
