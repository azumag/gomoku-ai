# -*- coding: utf-8 -*-

import tensorflow as tf

import csv
import time
import sys
import random

batch = 100
test_ratio = 0.1

# 開始時刻
start_time = time.time()
print "開始時刻: " + str(start_time)

# MNISTデータの読み込み
print "--- データの読み込み開始 ---"
histories = csv.reader(open('../data/lv5h', 'r'))
answs = csv.reader(open('../data/lv5a', 'r'))

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
init = tf.initialize_all_variables()

# Sessionを開始する
# runすることで初めて実行開始される（run(init)しないとinitが実行されない）

sess = tf.Session()
sess.run(init)

# train_stepを実行する
# feed_dictでplaceholderに値を入力することができる
print "--- 訓練開始 ---"
for i in range(len(hst_data)):
    print 'batch: ' + str(i)
    train_data  = hst_data[i: i+1*batch]
    train_label = ans_data[i: i+1*batch]
    sess.run(train_step, feed_dict={x: train_data, y_: train_label})
print "--- 訓練終了 ---"

# 正しいかの予測
# 計算された画像がどの数字であるかの予測yと正解ラベルy_を比較する
#同じ値であればTrueが返される
# argmaxは配列の中で一番値の大きい箇所のindexが返される
#一番値が大きいindexということは、それがその数字である確率が一番大きいということ
# Trueが返ってくるということは訓練した結果と回答が同じということ
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

# 精度の計算
# correct_predictionはbooleanなのでfloatにキャストし、平均値を計算する
# Trueならば1、Falseならば0に変換される
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# 精度の実行と表示
# テストデータの画像とラベルで精度を確認する
# ソフトマックス回帰によってWとbの値が計算されているので、xを入力することでyが計算できる
print "精度"
test_data  = hst_data[0: int(len(hst_data)*test_ratio)]
test_label = ans_data[0: int(len(ans_data)*test_ratio)]
print(sess.run(accuracy, feed_dict={x: test_data, y_: test_label}))


# 終了時刻
end_time = time.time()
print "終了時刻: " + str(end_time)
print "かかった時間: " + str(end_time - start_time)

saver = tf.train.Saver()
saver.save(sess, 'model/model.ckpt')


