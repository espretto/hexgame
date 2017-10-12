
import random

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

    def __eq__ (self, other):
        return self.x == other.x and self.y == other.y

    def __ne__ (self, other):
        return not self.__eq__(other)


class Game (object):

    def __init__ (self, cols=11, rows=11):
        self.cols = cols
        self.rows = rows
        self.board = [[0 for row in range(rows)] for col in range(cols)]

    def play (self, alice, bob):
        raise NotImplementedError()

    def isValid (self, tile):
        return self.contains(tile) and self.board[tile.x][tile.y] == EMPTY

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

                for neighbour in self.neighbours(tile):
                    if neighbour not in done:
                        todo.add(neighbour)

        return False
