# -*- coding: utf-8 -*-

import tensorflow as tf

import csv
import time
import sys
import random

batch = 1000
test_ratio = 0.1
log = argv[1]

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

# 開始時刻
start_time = time.time()
print "開始時刻: " + str(start_time)

# MNISTデータの読み込み
print "--- データの読み込み開始 ---"
histories = csv.reader(open('/home/azumagakito/gomoku-ai/ai/tmp/h-'+log, 'r'))
answs = csv.reader(open('/home/azumagakito/gomoku-ai/ai/tmp/a-'+log, 'r'))

hst_data = [ [ int(a) for a in v ] for v in histories]
ans_data = [ [ int(a) for a in v ] for v in answs]

print "--- データの読み込み完了 ---"

wc1 = weight_variable([5,5,1,81])
bc1 = bias_variable([81])

x = tf.placeholder(tf.float32, [None, 81])
y_ = tf.placeholder(tf.float32, [None, 81])

x_image = tf.reshape(x, [-1, 9,9, 1])

hc1 = tf.nn.relu(conv2d(x_image, wc1) + bc1)
hp1 = max_pool_2x2(hc1)

W_conv2 = weight_variable([5, 5, 81, 32])
b_conv2 = bias_variable([32])

h_conv2 = tf.nn.relu(conv2d(hp1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([3*3*32, 81])
b_fc1 = bias_variable([81])

h_pool2_flat = tf.reshape(h_pool2, [-1, 3*3*32])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([81, 81])
b_fc2 = bias_variable([81])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2


cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

for i in range(len(hst_data)):
  train_data  = hst_data[i: i+1*batch]
  train_label = ans_data[i: i+1*batch]
        
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={ x:train_data, y_: train_label, keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))

  train_step.run(feed_dict={x: train_data, y_: train_label, keep_prob: 0.5})

test_data  = hst_data[0: int(len(hst_data)*test_ratio)]
test_label = ans_data[0: int(len(ans_data)*test_ratio)]
print("test accuracy %g"%accuracy.eval(feed_dict={
    x: test_data, y_: test_label, keep_prob: 1.0}))


# 終了時刻
end_time = time.time()
print "終了時刻: " + str(end_time)
print "かかった時間: " + str(end_time - start_time)

saver = tf.train.Saver()
saver.save(sess, '/home/azumagakito/gomoku-ai/ai/lv12/model/model.ckpt')


