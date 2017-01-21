import csv
import time

class Util:
    init_time = None

    def __init__(self):
        self.start_time = None

    def print_start(self):
        self.start_time = time.time()
        print "start time: " + str(self.start_time)

    def print_end(self):
        end_time = time.time()
        print "end time: " + str(end_time)
        print "processed: " + str(end_time - self.start_time)

    def load_data(self, path):
        print "--- start loading data ---"
        data = [[ int(a) for a in v ] for v in csv.reader(open(path, 'r'))]
        print "--- end loading data ---"
        return data
