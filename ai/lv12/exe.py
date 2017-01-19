import tensorflow as tf
import random
import csv
import sys
import os

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

wc1 = weight_variable([5,5,1,81])
bc1 = bias_variable([81])

x = tf.placeholder(tf.float32, [None, 81])

x_image = tf.reshape(x, [-1, 9,9, 1])

hc1 = tf.nn.relu(conv2d(x_image, wc1) + bc1)
hp1 = max_pool_2x2(hc1)

W_conv2 = weight_variable([5, 5, 81, 32])
b_conv2 = bias_variable([32])

h_conv2 = tf.nn.relu(conv2d(hp1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([3 * 3 * 32, 81])
b_fc1 = bias_variable([81])

h_pool2_flat = tf.reshape(h_pool2, [-1, 3*3*32])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([81, 81])
b_fc2 = bias_variable([81])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

init = tf.global_variables_initializer()
#
sess=tf.InteractiveSession()
sess.run(init)

saver = tf.train.Saver()
saver.restore(sess, os.path.dirname(__file__) + "/model/model.ckpt")

input_d = [[ int(i) for i in sys.argv[1:] ]]

print(sess.run(tf.argmax(y_conv, 1), feed_dict={x: input_d, keep_prob:0.5})[0])

