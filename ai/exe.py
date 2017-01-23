import common.board_manager as bm
import numpy as np
import random

import tensorflow as tf
import common.perceptron as nn
import sys

model_file = sys.argv[1]
board = [sys.argv[3:]]
layer = sys.argv[2]
b = bm.BoardManager()
n = nn.Perceptron(layer, 81, 81)
n.load(model_file)

result = n.execute(board)[0]
print result
