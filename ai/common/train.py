#-*- coding: utf-8 -*-

import tensorflow as tf
import perceptron as nn

accuracies = []

#for i in range(1, 10):
n = nn.Perceptron(4)
n.train('../tmp/h-4v4','../tmp/a-4v4', 1)
result = n.test('../tmp/h-4v4','../tmp/a-4v4')
accuracies.append(result)

print accuracies

