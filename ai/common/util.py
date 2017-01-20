import csv
import time

class util:
    init_time = None

    def __init__(self):
        self.init_time = None

    def print_init:
        self.init_time = time.time()
        print "開始時刻: " + str(self.init_time)

    def print_end:
        end_time = time.time()
        print "終了時刻: " + str(end_time)
        print "かかった時間: " + str(end_time - self.init_time)

    def load_data(path):
        print "--- データの読み込み開始 ---"
        data = csv.reader(open(path, 'r'))
        print "--- データの読み込み完了 ---"
        return data
