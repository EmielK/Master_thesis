import numpy as np

from MDP.constants import *


def new_job(v: np.ndarray) -> np.ndarray:
    """
    New job arrives in the system, which can happen in any system state. This
    only alters the stock value.
    """
    u = v.copy()

    for index in range(STOCK_SIZE):
        if index >= 3:
            u[:, :, :, :, index] = \
                (1 - PROB_NEW_JOBS) * v[:, :, :, :, index] + \
                PROB_NEW_JOBS * (PROB_1 * v[:, :, :, :, index - 1] +
                                 PROB_2 * v[:, :, :, :, index - 2] +
                                 PROB_3 * v[:, :, :, :, index - 3])
        elif index == 2:
            u[:, :, :, :, index] = \
                (1 - PROB_NEW_JOBS) * v[:, :, :, :, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[:, :, :, :, index - 1] +
                        (PROB_2 + PROB_3) * v[:, :, :, :, index - 2])
        elif index == 1:
            u[:, :, :, :, index] = \
                (1 - PROB_NEW_JOBS) * v[:, :, :, :, index] + \
                PROB_NEW_JOBS * v[:, :, :, :, index - 1]
        elif index == 0:
            u[:, :, :, :, index] = v[:, :, :, :, index]

    print("new job", '\n', u[:NUM_STATES, 0, 0, 0, :].round(1), '\n')
    return u
