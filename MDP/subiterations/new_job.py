import numpy as np

from MDP.constants import *


def new_job(v: np.ndarray, n):
    """
    New job arrives in the system, which can happen in any system state. This
    only alters the stock value.
    """
    for index in range(STOCK_SIZE):
        if index - 3 >= 0:
            v[n, :, :, :, :, index] = \
                (1 - PROB_NEW_JOBS) * v[n - 1, :, :, :, :, index] + \
                PROB_NEW_JOBS * (PROB_1 * v[n - 1, :, :, :, :, index - 1] +
                                 PROB_2 * v[n - 1, :, :, :, :, index - 2] +
                                 PROB_3 * v[n - 1, :, :, :, :, index - 3])
        elif index - 2 >= 0:
            v[n, :, :, :, :, index] = \
                (1 - PROB_NEW_JOBS) * v[n - 1, :, :, :, :, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[n - 1, :, :, :, :, index - 1] +
                        (PROB_2 + PROB_3) * v[n - 1, :, :, :, :, index - 2])
        elif index - 1 >= 0:
            v[n, :, :, :, :, index] = \
                (1 - PROB_NEW_JOBS) * v[n - 1, :, :, :, :, index] + \
                PROB_NEW_JOBS * v[n - 1, :, :, :, :, index - 1]
        elif index == 0:
            v[n, :, :, :, :, index] = v[n - 1, :, :, :, :, index]
