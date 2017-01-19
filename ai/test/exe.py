import tensorflow as tf
import random
import csv
import sys
import os

x = tf.placeholder(tf.float32, [None, 5])
W = tf.Variable(tf.zeros([5, 5]))
#W2 = tf.Variable(tf.zeros([5, 81]))
#W3 = tf.Variable(tf.zeros([5, 81]))
b = tf.Variable(tf.zeros([5]))
#b2 = tf.Variable(tf.zeros([5]))
#b3 = tf.Variable(tf.zeros([5]))
y = tf.nn.softmax(tf.matmul(x, W) + b)
#y2 = tf.nn.relu(tf.matmul(y, W2) + b2)
#y3 = tf.nn.softmax(tf.matmul(y2, W3) + b3)

init = tf.global_variables_initializer()

sess=tf.InteractiveSession()
sess.run(init)

saver = tf.train.Saver()
saver.restore(sess, "./model/model.ckpt")

#histories = csv.reader(open('../tmp/histries.dat', 'r'))
#hst_data = [ [ int(a) for a in v ] for v in histories]
#input_d = [random.choice(hst_data)]
input_d = [[ int(i) for i in sys.argv[1:] ]]
#print(input_d)
#print(len(input_d))

print(sess.run(tf.argmax(y, 1), feed_dict={x: input_d}))[0]

#print(os.path.dirname(__file__))

