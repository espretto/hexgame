
import asyncio

from hexgame import Game
from itertools import product

from alice import Player as Alice
from noname import Player as Noname
from mcts.IAbidon import Player as Mcts
from ironman import Player as Ironman
from bro import Player as Bro

class Participant (object):

    def __init__ (self, Player):
        self.player = Player()
        self.score = 0
        if hasattr(self.player, 'name'):
            self.name = self.player.name
        else:
            self.name = Player.name

    def __str__ (self):
        return '%s won %d times' % (self.name, self.score)


def pairs (players):
    for pair in product(players, repeat=2):
        if pair[0] != pair[1]:
            yield pair

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    game = Game(loop=loop)

    participants = [
        #Participant(Alice),
        Participant(Noname),
        Participant(Mcts),
        Participant(Ironman),
        Participant(Bro)
    ]

    results = {}
    winner = None
    looser = None

    for alice, bob in pairs(participants):
        for i in range(10):
            print('-' * 60)
            print('%s vs %s' % (alice.name, bob.name))
            looser, reason = game.play(alice.player, bob.player)
            game.reset()

            if looser == alice.player:
                looser = alice
                winner = bob
            else:
                looser = bob
                winner = alice

            winner.score += 1
            result = '%s beats %s' % (winner.name, looser.name)
            if not result in results:
                results[result] = 0
            results[result] += 1

    # print('-' * 60)
    # for participant in sorted(participants, key=lambda p: p.score):
    #     print(str(participant))
    # print('-' * 60)

    for result, count in results.items():
        print('%s: %d' % (result, count))
