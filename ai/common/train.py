#-*- coding: utf-8 -*-

import tensorflow as tf
import perceptron as nn

n = nn.Perceptron(3)
n.train('4v4',1000)

