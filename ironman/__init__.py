
from hexgame import AbstractPlayer, HORIZ, VERTI, EMPTY
from alice import Player as Alice

class Player (AbstractPlayer):

    name = 'Ironman'

    def __init__ (self):
        self.__vide__ = True
        self.__left__ = False
        self.__right__ = False
        self.__top__ = False
        self.__bottom__ = False

    def play(self, board, direction, **options):

        cols = len(board)
        rows = len(board[0])

        if direction == HORIZ:

            if not self.__left__:

                for x in range(cols):

                    col = board[x]

                    if self.__left__:
                        break

                    for y in range(rows):

                        if col[y] == direction:
                            self.__vide__ = False
                            self.__left__ = x == 0

                            if self.__left__:
                                break

                            elif 0 <= x-1 and board[x-1][y] == EMPTY:
                                return (x-1, y)
                            elif 0 <= y-1 and board[x][y-1] == EMPTY:
                                return (x, y-1)
                            elif 0 <= x-1 and y+1 < rows and board[x-1][y+1] == EMPTY:
                                return (x-1, y+1)

            if not self.__right__:

                for x in reversed(range(cols)):

                    col = board[x]

                    if self.__right__:
                        break

                    for y in range(rows):

                        if col[y] == direction:
                            self.__vide__ = False
                            self.__right__ = x == cols-1

                            if self.__right__:
                                break

                            if x+1 < cols and board[x+1][y] == EMPTY:
                                return (x+1, y)
                            elif y+1 < rows and board[x][y+1] == EMPTY:
                                return (x, y+1)
                            elif x+1 < cols and 0 <= y-1 and board[x+1][y-1] == EMPTY:
                                return (x+1, y-1)

            if self.__vide__:
                x = cols // 2
                y = rows // 2
                return (x, y) if board[x][y] == EMPTY else (x-1, y)
            else:
                return Alice().play(board, direction)

        elif direction == VERTI:

            if not self.__top__:

                for y in range(rows):

                    if self.__top__:
                        break

                    for x in range(cols):

                        if board[x][y] == direction:
                            self.__vide__ = False
                            self.__top__ = y == 0

                            if self.__top__:
                                break

                            elif 0 <= y-1 and board[x][y-1] == EMPTY:
                                return (x, y-1)
                            elif x+1 < cols and 0 <= y-1 and board[x+1][y-1] == EMPTY:
                                return (x+1, y-1)

            if not self.__bottom__:

                for y in reversed(range(rows)):

                    if self.__bottom__:
                        break

                    for x in range(cols):

                        if board[x][y] == direction:
                            self.__vide__ = False
                            self.__bottom__ = y == rows-1

                            if self.__bottom__:
                                break

                            elif 0 <= x-1 and y+1 < rows and board[x-1][y+1] == EMPTY:
                                return (x-1, y+1)
                            elif y+1 < rows and board[x][y+1] == EMPTY:
                                return (x, y+1)

            if self.__vide__:
                x = cols // 2
                y = rows // 2
                return (x, y) if board[x][y] == EMPTY else (x, y+1)
            else:
                return Alice().play(board, direction)
