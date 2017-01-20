#-*- coding: utf-8 -*-

import tensorflow as tf
import perceptron as nn
import util as u

#for i in range(1, 10):
n = nn.Perceptron(4, 81, 81)
n.load('./testsave/save.ckpt')
util = u.Util()
data_sample = util.load_data('../tmp/h-4v4')
result = n.execute(data_sample)

print result
print len(result)
