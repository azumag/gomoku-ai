import numpy as np

class Boardmanager:
    BOARD_SIZE = 9
    board = np.zeros([BOARD_SIZE, BOARD_SIZE])

    def __init__(self):
        print('init')
        print board
