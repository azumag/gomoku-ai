import board_manager as bm
import numpy as np
import random

import tensorflow as tf
import perceptron as nn

b = bm.BoardManager()
n = nn.Perceptron(4, 81, 81)
n.load('./testsave/save.ckpt')

turn = 1
while True:
    board = np.zeros([b.BOARD_SIZE, b.BOARD_SIZE])
    while True:

        result = n.execute(board.reshape([1, 81]))[0]
        i = result / b.BOARD_SIZE
        j = result - (b.BOARD_SIZE*i)
        print result,i,j

        # prior: board is not filled
        while (board[i][j] != 0):
            i = random.randint(0, 8)
            j = random.randint(0, 8)

        board[i][j] = turn

        b.print_board(board)

        status = b.status(board)
        if status == 1:
            print 'win'
            break
        elif status == 2:
            print 'lose'
            break
        elif status == 3:
            print 'draw'
            break
        else:
            print 'none'

        turn = b.switch_turn(turn)
        print '====='
