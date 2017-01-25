import common.board_manager as bm
import common.perceptron as nn
import sys


model_file = sys.argv[2]
data_file_d = sys.argv[3]
data_file_l = sys.argv[4]

layer = int(sys.argv[1])

b = bm.BoardManager()
n = nn.Perceptron(layer, 81, 81)

n.train(data_file_d, data_file_l, 1)
n.save(model_file)

