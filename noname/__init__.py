import time
import random
from hexgame import AbstractPlayer

class Player (AbstractPlayer):

    name = 'noname'

    def play(self, board, direction, **options):
        self.start_time = time.time()
        self.max_time = 0.4
        first_play = True
        player = direction
        self.name = "Omae wa\nShindeiru...\n\n...Pitetre"

        for a in range(len(board)):
            if (board[a].count(1) or board[a].count(-1)):
                first_play = False

        if (first_play):
            board[int(len(board)/2)][int(len(board)/2)] = player
            return (int(len(board)/2), int(len(board)/2))
        else:
            max = -10000
            i = 0
            j = 0
            maxi = 0
            maxj = 0
            tmp = 0
            if(player == -1):
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[i][j] == 0 and (time.time() - self.start_time < 0.5):
                            board[i][j] = player
                            tmp = self.Min(board, 3, player)
                            if tmp > max or ((tmp == max) and (random.randint(0, 1000) % 2 == 0)):
                                max = tmp
                                maxi = i
                                maxj = j
                            board[i][j] = 0

                return (maxi, maxj)
            else :
                for i in range(len(board)):
                    for j in range(len(board)):
                        if board[j][i] == 0 and (time.time() - self.start_time < 0.5):
                            board[j][i] = player
                            tmp = self.Min(board, 3, player)
                            if tmp > max or ((tmp == max) and (random.randint(0, 1000) % 2 == 0)):
                                max = tmp
                                maxi = i
                                maxj = j
                            board[i][j] = 0

                return (maxj, maxi)


    def Max(self, board, profondeur, joueur):
        if profondeur == 0 or (time.time() - self.start_time > 0.5) :
            return self.EvaluationFunction(board, self.last_position, joueur)
        else:
            max = -10000
            i = 0
            j = 0
            tmp = 0

            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == 0:
                        board[i][j] = joueur
                        self.last_position = (i, j)
                        tmp = self.Min(board, profondeur - 1, joueur)
                        if (tmp > max or ((tmp == max) and (random.randint(0, 1000) % 2 == 0))):
                            max = tmp
                        board[i][j] = 0

            return max

    def Min(self, board, profondeur, joueur):
        if profondeur == 0 or (time.time() - self.start_time > 0.5) :
            return self.EvaluationFunction(board, self.last_position, joueur)
        else:
            min = 10000
            i = 0
            j = 0
            tmp = 0

            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == 0:
                        board[i][j] = joueur
                        self.last_position = (i, j)
                        tmp = self.Max(board, profondeur - 1, joueur)
                        if (tmp < min or ((tmp == min) and (random.randint(0, 1000) % 2 == 0))):
                            min = tmp
                        board[i][j] = 0

            return min

    def EvaluationFunction(self, plateau, position, joueur):
        """fonction principale"""
        val = 0
        val += self.start_edge(plateau, position, joueur)
        val += self.bridge(plateau, position, joueur)
        val += self.close_bridge(plateau, position, joueur)
        return val

    def bridge(self, plateau, position, joueur):
        """test si bridge / retourne entre 0 et 12/14"""
        val = 0
        # bridge vertical
        if position[0] < len(plateau) - 1 and position[1] > 1:
            if plateau[position[0] + 1][position[1] - 2] == joueur:
                if joueur == -1:
                    val += 3
                else:
                    val += 2
            if plateau[position[0] + 1][position[1] - 2] == 0:
                if joueur == -1:
                    val += 2
                else:
                    val += 1
        if position[0] > 0 and position[1] < len(plateau) - 2:
            if plateau[position[0] - 1][position[1] + 2] == joueur:
                if joueur == -1:
                    val += 3
                else:
                    val += 2
            if plateau[position[0] - 1][position[1] + 2] == 0:
                if joueur == -1:
                    val += 2
                else:
                    val += 1

        # bridge /
        if position[0] < len(position) - 2 and position[1] > 0:
            if plateau[position[0] + 2][position[1] - 1] == joueur:
                val += 2
            if plateau[position[0] + 2][position[1] - 1] == 0:
                val += 1
        if position[0] > 1 and position[1] < len(plateau) - 1:
            if plateau[position[0] - 2][position[1] + 1] == joueur:
                val += 2
            if plateau[position[0] - 2][position[1] + 1] == 0:
                val += 1

        # bridge \
        if position[0] > 0 and position[1] > 0:
            if plateau[position[0] - 1][position[1] - 1] == joueur:
                val += 2
            if plateau[position[0] - 1][position[1] - 1] == 0:
                val += 1
        if position[0] < len(plateau) - 1 and position[1] < len(plateau) - 1:
            if plateau[position[0] + 1][position[1] + 1] == joueur:
                val += 2
            if plateau[position[0] + 1][position[1] + 1] == 0:
                val += 1

        return val

    def start_edge(self, plateau, position, joueur):
        """premier joueur ou bord"""
        val = 0
        if plateau.count("0") == 121:
            if position[0] == position[1] == 5:
                val += 10
        if (position[0] == 0 or position[0] == len(plateau) - 1) and joueur == 1:
            val += 5
        if (position[1] == 0 or position[1] == len(plateau) - 1) and joueur == -1:
            val += 5
        return val

    def close_bridge(self, plateau, position, joueur):
        """test si fermeture d'un bridge / retourne entre 0 et 14"""
        val = 0

        # bridge vertical
        if position[0] < len(plateau) - 1 and 0 < position[1] < len(plateau) - 1:
            if plateau[position[0] + 1][position[1] - 1] == plateau[position[0]][position[1] + 1] == joueur:
                if joueur == -1:
                    val += 3
                else:
                    val += 2
        if position[0] > 0 and 0 < position[1] < len(plateau) - 1:
            if plateau[position[0]][position[1] - 1] == plateau[position[0] - 1][position[1] + 1] == joueur:
                if joueur == -1:
                    val += 3
                else:
                    val += 2

        # bridge /
        if 0 < position[0] < len(plateau) - 1 and position[1] < len(plateau) - 1:
            if plateau[position[0] + 1][position[1]] == plateau[position[0] - 1][position[1] + 1] == joueur:
                val += 2
        if 0 < position[0] < len(plateau) - 1 and 0 < position[1]:
            if plateau[position[0] + 1][position[1] - 1] == plateau[position[0] - 1][position[1]] == joueur:
                val += 2

                # bridge \
        if position[0] < len(plateau) - 1 and 0 < position[1]:
            if plateau[position[0]][position[1] - 1] == plateau[position[0] + 1][position[1]] == joueur:
                val += 2
        if 0 < position[0] and position[1] < len(plateau) - 1:
            if plateau[position[0] - 1][position[1]] == plateau[position[0]][position[1] + 1] == joueur:
                val += 2

        return val
