#-*- coding: utf-8 -*-

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
histories = csv.reader(open('../data/lv8h', 'r'))
answs = csv.reader(open('../data/lv8a', 'r'))

hst_data = [ [ int(a) for a in v ] for v in histories]
ans_data = [ [ int(a) for a in v ] for v in answs]


