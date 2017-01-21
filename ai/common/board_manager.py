import numpy as np
import sys

class BoardManager:
    BOARD_SIZE = 9
    WIN_SIZE = 5
    PRIMARY_SIGN   = 1
    SECONDARY_SIGN = 2

    def __init__(self):
        print('init')

    def check_row(self, board):
        for row in board:
            for col in row:
                if col == 0:
                    continue
                count = 0
                print col
                for k in row:
                    if col == k:
                        count += 1
                    else:
                        if count >= self.WIN_SIZE:
                            return col
        return 0

    def check_next(self, board, i, j, di, dj, count):
        if count >= self.WIN_SIZE:
            return True
        if i+di >= self.BOARD_SIZE or j+dj >= self.BOARD_SIZE:
            return False
        if board[i][j] == board[i+di][j+dj]:
            return self.check_next(board, i+di, j+dj, di, dj, count+1)
        else:
            return False

    def check(self, board, di, dj):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.check_next(board, i, j, di, dj, 1):
                    return board[i][j]

        return 0

    def status(self, board):

        status = self.check(board, 0, 1)

        if status != 0:
            return status

        status = self.check(board.T, 0, 1)

        if status != 0:
            return status

        status = self.check(board, 1, 1)

        if status != 0:
            return status

        status = self.check(np.fliplr(board), 1, 1)

        if status != 0:
            return status

        # check full
        filled = True
        for row in board:
            for col in row:
                if col == 0:
                    filled = False

        if filled:
            return 3

        return 0

    def print_board(self, board):
        for row in board:
            for col in row:
                if col == 0:
                    sys.stdout.write("+ ")
                elif col == 1:
                    sys.stdout.write("O ")
                else:
                    sys.stdout.write("X ")
            print ''

    def switch_turn(self, turn):
        if turn == 1:
            turn = 2
        else:
            turn = 1
        return turn
