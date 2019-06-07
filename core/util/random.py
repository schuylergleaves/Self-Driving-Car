import numpy as np


def get_random_sign():
    rand = np.random.randn()
    if rand > 0:
        return 1
    else:
        return -1