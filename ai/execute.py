import tensorflow as tf
import random
import csv
import sys
import os

x = tf.placeholder(tf.float32, [None, 81])
W = tf.Variable(tf.zeros([81, 81]))
b = tf.Variable(tf.zeros([81]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

init = tf.initialize_all_variables()

sess=tf.InteractiveSession()
sess.run(init)

saver = tf.train.Saver()
saver.restore(sess, os.path.dirname(__file__) + "/model.ckpt")

#histories = csv.reader(open('../tmp/histries.dat', 'r'))
#hst_data = [ [ int(a) for a in v ] for v in histories]
#input_d = [random.choice(hst_data)]
input_d = [[ int(i) for i in sys.argv[1:] ]]
#print(input_d)
#print(len(input_d))

print(sess.run(tf.argmax(y, 1), feed_dict={x: input_d}))[0]



