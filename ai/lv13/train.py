# -*- coding: utf-8 -*-

import tensorflow as tf

import csv
import time
import sys
import random

batch = 1
test_ratio = 0.1

# 開始時刻
start_time = time.time()
print "開始時刻: " + str(start_time)

# MNISTデータの読み込み
print "--- データの読み込み開始 ---"
histories = csv.reader(open('/home/azumagakito/gomoku-ai/ai/tmp/h-inf5', 'r'))
answs = csv.reader(open('/home/azumagakito/gomoku-ai/ai/tmp/a-inf5', 'r'))

hst_data = [ [ int(a) for a in v ] for v in histories]
ans_data = [ [ int(a) for a in v ] for v in answs]

print "--- データの読み込み完了 ---"

x = tf.placeholder(tf.float32, [None, 81])

# 重み
W = tf.Variable(tf.zeros([81, 81]))
#W2 = tf.Variable(tf.zeros([81, 81]))
#W3 = tf.Variable(tf.zeros([81, 81]))

# バイアス
b = tf.Variable(tf.zeros([81]))
#b2 = tf.Variable(tf.zeros([81]))
#b3 = tf.Variable(tf.zeros([81]))

# ソフトマックス回帰を実行
# yは入力x of 確率の分布
# matmul関数で行列xとWの掛け算を行った後、bを加算する。
# yは[1, 81]の行列
y = tf.nn.softmax(tf.matmul(x, W) + b)
#y2 = tf.nn.relu(tf.matmul(y, W2) + b2)
#y3 = tf.nn.softmax(tf.matmul(y2, W3) + b3)

# 交差エントロピー
# y_は正解データのラベル
y_ = tf.placeholder(tf.float32, [None, 81])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))

# 勾配法を用い交差エントロピーが最小となるようyを最適化する
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# 用意した変数Veriableの初期化を実行する
init = tf.global_variables_initializer()

# Sessionを開始する
# runすることで初めて実行開始される（run(init)しないとinitが実行されない）

sess = tf.Session()
sess.run(init)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

test_data  = hst_data[0: int(len(hst_data)*test_ratio)]
test_label = ans_data[0: int(len(ans_data)*test_ratio)]


# train_stepを実行する
# feed_dictでplaceholderに値を入力することができる
print "--- 訓練開始 ---"
for i in range(len(hst_data)):
    print 'batch: ' + str(i)
    train_data  = hst_data[i: i+1*batch]
    train_label = ans_data[i: i+1*batch]
    sess.run(train_step, feed_dict={x: train_data, y_: train_label})
    if i%1000 == 0:
        print(sess.run(accuracy, feed_dict={x: test_data, y_: test_label}))
print "--- 訓練終了 ---"


# 終了時刻
end_time = time.time()
print "終了時刻: " + str(end_time)
print "かかった時間: " + str(end_time - start_time)

saver = tf.train.Saver()
saver.save(sess, '/home/azumagakto/gomoku-ai/ai/lv13/model/model.ckpt')


