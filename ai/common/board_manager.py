import numpy as np

class BoardManager:
    BOARD_SIZE = 9
    PRIMARY_SIGN   = 1
    SECONDARY_SIGN = 2
    board = np.zeros([BOARD_SIZE, BOARD_SIZE])

    def __init__(self):
        print('init')
        print self.board

    def status(self, board):
        line = 0
        for i in xrange(BOARD_SIZE):
            if board[0][i] != 0:
                line = 1
                for j in xrange(BORAD_SIZE):
                    if board[0][i] != board[j][i]:
                        line = 0
                        break
            else:
                line = 0

        if line != 0:
            return board[0][i]

        for i in xrange(BOARD_SIZE):
            if board[i][0] != 0:
                line = 1
                for j in xrange(BOARD_SIZE):
                    if board[i][0] != board[j][i]:
                        line = 0
                        break
            else:
                line=0

        if line != 0:
            return board[i][0]

        for i in xrange(1, BOARD_SIZE):
            if board[0][0] != 0:
                line = 1
                if board[0][0] != board[i][i]:
                    line = 0
                    break
            else:
                line = 0

        if line != 0:
            return board[0][0]

        for i in xrange(1, BOARD_SIZE):
            if board[0][BOARD_SIZE-1] != 0:
                line = 1
                if board[0][BOARD_SIZE-1] != board[i][BOARD_SIZE-1-i]:
                    line = 0
                    break
            else:
                line = 0

        if line != 0:
            return board[0][BOARD_SIZE-1]

        for i in xrange(BOARD_SIZE):
            for j in xrange(BOARD_SIZE):
                if board[i][j]==0:
                    return 0

        return 3
