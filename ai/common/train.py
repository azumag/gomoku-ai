#-*- coding: utf-8 -*-

import tensorflow as tf
import perceptron as nn
import util as u

accuracies = []

#for i in range(1, 10):
n = nn.Perceptron(4, 81, 81)
n.train('../tmp/h-4v4','../tmp/a-4v4', 1)
data_sample = u.Util().load_data('../tmp/h-4v4')
result = n.execute(data_sample)
accuracies.append(result)

print accuracies
