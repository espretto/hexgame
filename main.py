
import asyncio

from hexgame import Game
from alice import Player as Alice
from bob import Player as Bob

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    game = Game(loop=loop)

    bob = Alice()
    alice = Alice()

    game.play(alice, bob)
