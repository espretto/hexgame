
from hexgame import Game
from alice import Player as Alice
from bob import Player as Bob

if __name__ == '__main__':
    game = Game()

    alice = Alice()
    bob = Bob()

    game.play(alice, bob)
