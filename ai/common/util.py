import csv
import time

class util:
    init_time = None

    def __init__(self):
        # 開始時刻
        self.init_time = time.time()
        self.print_init

    def print_init:
        print "開始時刻: " + str(self.init_time)

    def load_data(path):
        print "--- データの読み込み開始 ---"
        data = csv.reader(open(path, 'r'))
        print "--- データの読み込み完了 ---"
        return data

  
