import common.board_manager as bm
import common.perceptron as nn

import numpy as np
import random

import tensorflow as tf


layer = sys.argv[1]
model_file = sys.argv[2]
data_file_d = sys.argv[3]
data_file_l = sys.argv[4]

b = bm.BoardManager()
n = nn.Perceptron(layer, 81, 81)

n.load(model_file)

train_n = 10 # number of train battle
count = 0

b.clear_data(data_file_d)
b.clear_data(data_file_l)

while True:
    if count >= train_n:
        count = 0
        n.train(data_file_d, data_file_l, 1)
        n.save(model_file)
        b.clear_data(data_file_d)
        b.clear_data(data_file_l)
    count += 1

    turn = 1
    board = np.zeros([b.BOARD_SIZE, b.BOARD_SIZE])
    board_histories = [[], []]
    answer_histories = [[],[]]
    while True:

        result = n.execute(b.transform_bridge(board))[0]
        i = result / b.BOARD_SIZE
        j = result - (b.BOARD_SIZE*i)
        # print result,i,j

        # prior: board is not filled
        while (board[i][j] != 0):
            i = random.randint(0, len(board)-1)
            j = random.randint(0, len(board)-1)

        # write histories
        # print board
        history = np.array(b.transform_bridge(board)[0])
        if turn == 2:
            # convert 1 to 2, 2 to 1 if turn == 2
            history[history==1] = -1
            history[history==2] = -2
            history[history==-1] = 2
            history[history==-2] = 1
        board_histories[turn-1].append(history)

        board[i][j] = turn

        # create zeroshot answer
        answer = np.zeros([b.BOARD_SIZE, b.BOARD_SIZE])
        answer[i][j] = 1
        answer_histories[turn-1].append(np.array(b.transform_bridge(answer)[0]))

        status = b.status(board)
        if status in (1, 2):
            print 'win: ' + str(turn)
            # print (board_histories)
            # print len(board_histories)
            # b.print_history(board_histories)
            b.save_data(data_file_d, board_histories[turn-1], 'a')
            b.save_data(data_file_l, answer_histories[turn-1], 'a')
            break
        elif status == 3:
            print 'draw'
            break
        else:
            pass

        turn = b.switch_turn(turn)
    # break
