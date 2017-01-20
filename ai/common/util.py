import csv
import time

class Util:
    init_time = None

    def __init__(self):
        self.init_time = None

    def print_init():
        self.init_time = time.time()
        print "start time: " + str(self.init_time)

    def print_end():
        end_time = time.time()
        print "end time: " + str(end_time)
        print "processed: " + str(end_time - self.init_time)

    def load_data(self, path):
        print "--- start loading data ---"
        data = csv.reader(open(path, 'r'))
        print "--- end loading data ---"
        return data
