
import copy
import random
import asyncio
import concurrent

EMPTY = 0
HORIZ = 1
VERTI = -1

class AbstractPlayer (object):

    def play (self, board, direction, **options):
        raise NotImplementedError()


class Tile (object):

    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.z = x+y

    def __hash__ (self):
        return self.x & (self.y << 8) & (self.z << 16)

    def __eq__ (self, other):
        return self.x == other.x and self.y == other.y

    def __ne__ (self, other):
        return not self.__eq__(other)


class Game (object):

    def __init__ (self, cols=11, rows=11, timeout=0.5, loop=None):
        self.loop = loop
        self.cols = cols
        self.rows = rows
        self.board = [[0 for row in range(rows)] for col in range(cols)]
        self.boardcopy = copy.deepcopy(self.board)
        self.timeout = timeout
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def reset (self):
        for x in range(self.cols):
            for y in range(self.rows):
                self.board[x][y] = EMPTY
                self.boardcopy[x][y] = EMPTY

    def play (self, alice, bob):

        # choose initial player and direction pseudo-randomly
        player = bob
        direction = HORIZ if random.random() > 0.5 else VERTI

        # play as long as the game is not finished
        while not self.isFinished(direction):

            # swap player for next iteration
            player = bob if player == alice else alice
            direction = HORIZ if direction == VERTI else VERTI
            name = 'horiz' if direction == HORIZ else 'verti'

            # clone the board for the player to manipulate
            for x in range(self.cols):
                for y in range(self.rows):
                    self.boardcopy[x][y] = self.board[x][y]

            # let play until timeout
            task = self.loop.run_in_executor(self.executor, player.play, self.boardcopy, direction)
            future = asyncio.wait_for(task, self.timeout)

            try:
                x, y = self.loop.run_until_complete(future)
            except concurrent.futures.TimeoutError:
                return player, 'timeout'

            # debug
            # print(name, ' (%d,%d)' % (x, y))

            # validation
            if not self.isValid(Tile(x, y)):
                return player, 'false play'

            # modify the board
            self.board[x][y] = direction

        # and the looser is...
        player = bob if player == alice else alice
        direction = HORIZ if direction == VERTI else VERTI
        name = 'horiz' if direction == HORIZ else 'verti'

        return player, 'KO'

    def at (self, tile):
        return self.board[tile.x][tile.y]

    def isValid (self, tile):
        return self.contains(tile) and self.at(tile) == EMPTY

    def contains (self, tile):
        return 0 <= tile.x < self.cols and 0 <= tile.y < self.rows

    def neighbours (self, tile):

        neighbours = [
            Tile(tile.x+1, tile.y  ),
            Tile(tile.x-1, tile.y  ),
            Tile(tile.x+1, tile.y-1),
            Tile(tile.x-1, tile.y+1),
            Tile(tile.x,   tile.y-1),
            Tile(tile.x,   tile.y+1)
        ]

        return [tile for tile in neighbours if self.contains(tile)]

    def isFinished (self, direction):

        # stupid test first
        nempty = 0
        for x in range(self.cols):
            for y in range(self.rows):
                if self.board[x][y] == EMPTY:
                    nempty += 1

        if nempty == 0:
            return True

        # dijstra
        if direction == HORIZ:
            x = self.cols-1
            origins = [Tile(0, y) for y in range(self.rows) if self.board[0][y] == direction]
            destins = [Tile(x, y) for y in range(self.rows) if self.board[x][y] == direction]
        elif direction == VERTI:
            y = self.rows-1
            origins = [Tile(x, 0) for x in range(self.cols) if self.board[x][0] == direction]
            destins = [Tile(x, y) for x in range(self.cols) if self.board[x][y] == direction]

        if not origins or not destins:
            return False

        # breath-first search for a connection between two opposite borders
        todo = set()
        done = set()

        for origin in origins:
            todo.clear()
            done.clear()

            todo.add(origin)

            while todo:
                tile = todo.pop()

                if tile in destins:
                    return True

                done.add(tile)

                for tile in self.neighbours(tile):
                    if self.at(tile) == direction and tile not in done:
                        todo.add(tile)

        return False

    def __str__ (self):
        upperedge = '\  /'
        loweredge = ' \/ '
        lines = []

        def cap (d):
            return 'H' if d == HORIZ else 'V' if d == VERTI else ' '

        for y in range(self.rows):
            indent = '  ' * y
            lines.append(indent + self.cols*upperedge + '\\')
            lines.append(indent + self.cols*loweredge + ' \\')
            row = [cap(self.board[x][y]) for x in range(self.cols)]
            lines.append(indent + ' | ' + ' | '.join(row) + ' |')

        # fix first line
        lines[0] = '  ' + lines[0][2:]
        lines[1] = '  ' + lines[1][2:]

        # fix last line
        indent += '  '
        lines.append(indent + self.cols*upperedge)
        lines.append(indent + self.cols*loweredge)

        return '\n'.join(lines)
