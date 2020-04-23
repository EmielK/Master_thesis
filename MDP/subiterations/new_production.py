import numpy as np

from ..constants import *


def new_production(v: np.ndarray, n: int, action: np.ndarray):
    """
    Computes the optimal choice regarding whether to start a new production
    cycle or not and assigns this value this value to the value array.
    """
    for T in range(1, MAX_MAIN_TIME):
        # If maintenance is being performed nothing changes.
        v[n, :, :, :, T, :] = v[n - 1, :, :, :, T, :]
        action[n, :, :, :, T, :] = DN
    for L in range(1, MAX_PROD_TIME):
        # If a job is not done don't start a new one.
        v[n, :, :, L, :, :] = v[n - 1, :, :, L, :, :]
        action[n, :, :, L, :, :] = DN
    # Do not start a new job if stock is full
    v[n, :, :, :, :, STOCK_SIZE - 1] = v[n - 1, :, :, :, :, STOCK_SIZE - 1]
    action[n, :, :, :, :, STOCK_SIZE - 1] = DN

    # Do nothing or start new production.
    v[n, :, 0, 0, 0, :STOCK_SIZE - 1] = \
        np.minimum(v[n - 1, :, DN, DN, 0, :STOCK_SIZE - 1],
                   v[n - 1, :, PROD_1, PROD_LEN_1, 0, :STOCK_SIZE - 1])

    action[n, :, 0, 0, 0, :STOCK_SIZE - 1] = \
        np.argmin([v[n - 1, :, DN, DN, 0, :STOCK_SIZE - 1],
                   v[n - 1, :, PROD_1, PROD_LEN_1, 0, :STOCK_SIZE - 1]],
                  axis=0)
