import numpy as np

class Boardmanager:
    board = np.meshgrid(np.zeros(9))

    def __init__(self):
        print('init')
        print board
