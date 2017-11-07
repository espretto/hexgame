from hexgame import AbstractPlayer, HORIZ, VERTI, EMPTY, Tile, Game
import random
import copy

class BroGame (Game):
    def setBoard(self, board):
        self.board = board
        self.boardcopy = copy.deepcopy(self.board)

    def communNeighbours(self, tile1, tile2):
        neighbours1 = self.neighbours(tile1)
        neighbours2 = self.neighbours(tile2)

        return [tile for tile in neighbours1 if tile in neighbours2]

    def freeCommunNeighbours(self, tile1, tile2):
        neighbours1 = self.freeNeighbours(tile1)
        neighbours2 = self.freeNeighbours(tile2)


        return [tile for tile in neighbours1 if (tile in neighbours2) and (self.board[tile.x][tile.y] == EMPTY)]

    def occupCommunNeighbours(self, tile1, tile2,direction):
        neighbours1 = self.freeNeighbours(tile1)
        neighbours2 = self.freeNeighbours(tile2)

        return [tile for tile in neighbours1 if (self.board[tile.x,tile.y] != direction and self.board[tile.x,tile.y] != Empty)]

    def freeNeighbours (self, tile):
        neighbours = []
        if(self.board[tile.x+1][tile.y] == Empty):
            neighbours.append(Tile(tile.x+1, tile.y))

        if(self.board[tile.x-1][tile.y] == Empty):
            neighbours.append(Tile(tile.x-1, tile.y))

        if(self.board[tile.x+1][tile.y-1] == Empty):
            neighbours.append(Tile(tile.x+1, tile.y-1))

        if(self.board[tile.x-1][tile.y+1] == Empty):
            neighbours.append(Tile(tile.x-1, tile.y+1))

        if(self.board[tile.x][tile.y-1] == Empty):
            neighbours.append(Tile(tile.x,   tile.y-1))

        if(self.board[tile.x][tile.y+1] == Empty):
            neighbours.append(Tile(tile.x,   tile.y+1))

        return [tile for tile in neighbours if self.contains(tile)]

    def occupNeighbours(self, tile, direction):
        neighbours = []
        if(self.board[tile.x+1][tile.y] != direction and self.board[tile.x+1][tile.y] != Empty ):
            neighbours.append(Tile(tile.x+1, tile.y))

        if(self.board[tile.x-1][tile.y] != direction and self.board[tile.x+1][tile.y] != Empty):
            neighbours.append(Tile(tile.x-1, tile.y))

        if(self.board[tile.x+1][tile.y-1] != direction and self.board[tile.x+1][tile.y] != Empty):
            neighbours.append(Tile(tile.x+1, tile.y-1))

        if(self.board[tile.x-1][tile.y+1] != direction and self.board[tile.x+1][tile.y] != Empty):
            neighbours.append(Tile(tile.x-1, tile.y+1))

        if(self.board[tile.x][tile.y-1] != direction and self.board[tile.x+1][tile.y] != Empty):
            neighbours.append(Tile(tile.x,   tile.y-1))

        if(self.board[tile.x][tile.y+1] != direction and self.board[tile.x+1][tile.y] != Empty):
            neighbours.append(Tile(tile.x,   tile.y+1))

        return [tile for tile in neighbours if self.contains(tile)]

class Player (AbstractPlayer):

    name = 'BroPlayer'

    #Variables globales pour le maintien d'information
    global minWay

    def __init__(self):

        #Variables pour placement des pions
        self._nbTurn = 0
        self._Horizontal = EMPTY
        self._BroGame = BroGame(rows=5, cols=5)
        self._Name = 'BroPlayer'

    #Fonction communicant avec le plateau
    def play(self, board, direction, **options):
        cols = len(board)
        rows = len(board[0])
        pointMap = [[0 for row in range(rows)] for col in range(cols)]

        if (self._nbTurn == 0):
            self.BroGame = Game(rows, cols)
            self._dir = direction
            if(direction == HORIZ):
                pass #print('Bro est horizontal')
            else:
                pass #print('Bro est vertical')

            x = int((cols+1)/2) if cols%2 == 1 else int(cols/2)
            y = int((rows+1)/2) if rows%2 == 1 else int(rows/2)

            if(board[x][y] != EMPTY):
                if(self._dir == HORIZ):
                    x -= 1
                    y += 1
                else:
                    x += 1
                    y -= 1

        else:
            BroMoves = []
            BadMoves = []

            self._BroGame.setBoard(board)

            for x in range (cols,1):
                for y in range(rows,1):
                    if(board[x][y] == self._dir):
                        BroMoves.append(Tile(x,y))
                    elif(board[x][y] != self._dir and board[x][y] != EMPTY):
                        BadMoves.append(Tile(x,y))


            for badMove in BadMoves:
                badDirection = Horiz if self._dir == VERTI else VERTI
                badNeighbours = self._BroGame.neighBours(badMove)
                for badNeighbour in badNeighbours:
                    badNeighbours2 =  self._BroGame.neighbours(badNeighbour)
                    for badNeighbour2 in badNeighbours2:
                        commBadNeighbours = self._BroGame.freeCommunNeighbours(badMove, badNeighbour2)
                        occupCommBadNeighbours = self._BroGame.occupCommunNeighbours(badMove,badNeighbour2,badDirection)
                        commBadNeighbours = self._BroGame.freeCommunNeighbours(badMove, badNeighbour2)
                        if(badNeighbour2 != self._dir and len(occupCommBadNeighbours)==1):
                            pointMap[commBadNeighbours[0].x][commBadNeighbours[0].y] += 11



            for broMove in BroMoves:
                neighbours = self._BroGame.neighbours(broMove)
                for neighbour in neighbours:
                    neighbours2 = self._BroGame.neighbours(neighbour)
                    for neighbour2 in neighbours2:
                        commNeighbours = self._BroGame.freeCommunNeighbours(broMove, neighbour2)
                        if(neighbour2 == EMPTY):
                            if(len(commNeighbours) == 1):
                                if(minDistanceWithObjective(broMove,rows,cols) <= minDistanceWithObjective(neighbour2,rows,cols)):
                                    pointMap[neighbour2.x][neighbour2.y] += 1
                                else:
                                    pointMap[neighbour2.x][neighbour2.y] += 3
                            elif(len(commNeighbours) == 2):
                                if(minDistanceWithObjective(broMove,rows,cols) <= minDistanceWithObjective(neighbour2,rows,cols)):
                                    pointMap[neighbour2.x][neighbour2.y] += 5
                                else:
                                    pointMap[neighbour2.x][neighbour2.y] += 7
                        elif(neighbour2 != self._dir):
                            if(len(commNeighbours)==2):
                                pointMap[commNeighbour[0].x][commNeighbour[0].y] += 2
                                pointMap[commNeighbour[1].x][commNeighbour[1].y] += 2
                            elif(len(commNeighbours)==1):
                                occupCommNeighbours = self._BroGame.occupCommunNeighbours(broMove,neighbour2,self._dir)
                                if(len(occupCommNeighbours) == 1):
                                    pointMap[commNeighbour[0].x][commNeighbour[0].y] += 0
                                else:
                                    pointMap[commNeighbour[0].x][commNeighbour[0].y] += 4


                        else:
                            begin = False
                            end = False
                            if(self._dir == HORIZ):
                                for y in range (1,rows):
                                    if(board[0][y] == self._dir):
                                        begin = True
                                    if(board[cols-1][y] == self._dir):
                                        start = True
                            else:
                                for x in range (1,cols):
                                    if(board[x][0] == self._dir):
                                        begin = True
                                    if(board[x][rows-1] == self._dir):
                                        start = True

                                if(start and begin):
                                    if(len(commNeighbours==2)):
                                        pointMap[commNeighbour[0].x][commNeighbour[0].y] += 8
                                        pointMap[commNeighbour[1].x][commNeighbour[1].y] += 8
                                if(len(commNeighbour==1)):
                                    pointMap[commNeighbour[0].x][commNeighbour[0].y] += 12


        maxValue = 0
        maxX = 0
        maxY = 0

        for x in range (len(pointMap),1):
            for y in range (len(pointMap[0])):
                if(pointMap[x][y]>maxValue):
                    maxValue = pointMap[x][y]
                    maxX = x
                    maxY = y

        if(maxValue == 0):
            x = random.randrange(cols)
            y = random.randrange(rows)

            while board[x][y] != EMPTY:
                x = random.randrange(cols)
                y = random.randrange(rows)
        else:
            x = maxX
            y = maxY

        self._nbTurn+=1


        return (x, y)

    #Explore le plateau à une distance de 1 d'un pion:
    #[ i,j-1 ];[i+1,j-1];[ i-1,j ];[ i+1,j ];[i-1,j+1];[ i,j+1 ] (x=i,y=j)


    #Explore le plateau à une distance de 2 d'un pion:
    #[i+1,j-1];[i-1,j-1];[i+2,j-1];[i-2,j+1];[i+1,j+1];[i-1,j+2] (x=i,y=j)


    def distanceBetweenBros(self,tile1,tile2):
        if(tile1.x == tile2.x and tile1.y == tile2.y):
            return 0
        elif(tile1.x == tile2.x):
            return abs(tile1.y - tile2.y)
        elif(tile1.x == tile2.x):
            return abs(tile1.x - tile2.x)
        else:
            return abs(tile1.x - tile2.x) + abs(tile1.y - tile2.y)

    def minDistanceWithObjective(self,tile,rows,cols):
        distances = []
        if(self._dir == HORIZ):
            for y in range (1,rows):
                distances.append(self.distanceBetweenBros(tile(0,y)))
                distances.append(self.distanceBetweenBros(tile(cols-1,y)))
        else:
            for x in range (1,cols):
                distances.append(self.distanceBetweenBros(tile(x,0)))
                distances.append(self.distanceBetweenBros(tile(x,rows-1)))

        return min(distance in distances)
