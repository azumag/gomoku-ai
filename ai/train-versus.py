import common.board_manager as bm
import common.perceptron as nn
import sys
import numpy as np
import random


model_file = sys.argv[2]
data_file_d = sys.argv[3]
data_file_l = sys.argv[4]

layer = int(sys.argv[1])

b = bm.BoardManager()
n = nn.Perceptron(layer, 81, 81)

n.train(data_file_d, data_file_l, 1)
n.save(model_file)
n.load(model_file)

n2 = nn.Perceptron(0, 81, 81)

ns = [n, n2]

count = 0

n_battle = int(sys.argv[5])


wins = [0, 0]

while True:
    count += 1
    if count >= n_battle:
        print wins
        print ( float(wins[0]) / n_battle )
        print ( float(wins[1]) / n_battle )
        break

    turn = 1
    board = np.zeros([b.BOARD_SIZE, b.BOARD_SIZE])
    board_histories = [[], []]
    answer_histories = [[],[]]
    finish = False
    while True:
        if finish:
            break

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

            #b.print_board(board)

            status = b.status(board)
            if status in (1, 2):
                print 'win: ' + str(turn)
                if turn == 1:
                    wins[0] += 1
                else:
                    wins[1] += 1
                finish = True
                break
            elif status == 3:
                print 'draw'
                finish = True
                break
            else:
                pass

            turn = b.switch_turn(turn)
    #
