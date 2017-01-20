#-*- coding: utf-8 -*-

import tensorflow as tf
import perceptron as nn
import util as u

accuracies = []

#for i in range(1, 10):
n = nn.Perceptron(4, 81, 81)
n.load('./testsave/save.ckpt')
data_sample = u.Util().load_data('../tmp/h-4v4')
result = n.execute(data_sample)
accuracies.append(result)

print accuracies
