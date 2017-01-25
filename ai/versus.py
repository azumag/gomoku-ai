import common.board_manager as bm
import common.perceptron as nn

import numpy as np
import random

import tensorflow as tf
import sys


model_file1 = sys.argv[1]
layer1 = int(sys.argv[2])

model_file2 = sys.argv[3]
layer2 = int(sys.argv[4])

b = bm.BoardManager()
n1 = nn.Perceptron(layer1, 81, 81)
n1.load(model_file1)

n2 = nn.Perceptron(layer2, 81, 81)
n2.load(model_file2)

ns = [n1, n2]

n_battle = int(sys.argv[5])
count = 0

#b.clear_data(data_file_d)
#b.clear_data(data_file_l)

wins = [0, 0]

while True:
    count += 1
    if count >= n_battle:
        print ( wins[0] / n_battle )
        print ( wins[1] / n_battle )

    turn = 1
    board = np.zeros([b.BOARD_SIZE, b.BOARD_SIZE])
    board_histories = [[], []]
    answer_histories = [[],[]]
    while True:

        for n in ns:

            board_bridge = np.array(b.transform_bridge(board))
            if turn == 2:
                board_bridge[board_bridge==1] = -1
                board_bridge[board_bridge==2] = -2
                board_bridge[board_bridge==-1] = 2
                board_bridge[board_bridge==-2] = 1

            result = n.execute(board_bridge)[0]
            i = result / b.BOARD_SIZE
            j = result - (b.BOARD_SIZE*i)
            # print result,i,j

            # prior: board is not filled
            while (board[i][j] != 0):
                i = random.randint(0, len(board)-1)
                j = random.randint(0, len(board)-1)

            board[i][j] = turn

            status = b.status(board)
            if status in (1, 2):
                print 'win: ' + str(turn)
                if turn == 1:
                    wins[0] += 1
                else:
                    wins[1] += 1
                break
            elif status == 3:
                print 'draw'
                break
            else:
                pass

            turn = b.switch_turn(turn)
    # break
