import numpy as np

from ..constants import *


def new_production(v: np.ndarray, action: np.ndarray) -> np.ndarray:
    """
    Computes the optimal choice regarding whether to start a new production
    cycle or not and assigns this value this value to the value array.
    """
    u = v.copy()

    """
    Select cheapest option, where the options are doing nothing or starting a 
    new production with setting i. This can only be done if there is no ongoing
    maintenance or production, the system is not in the failed state and the 
    stock is at capacity.
    """
    u[:NUM_STATES, 0, 0, 0, :TOTAL_SIZE - 1] = \
        np.minimum.reduce(
            [v[:NUM_STATES, DN, DN, 0, :TOTAL_SIZE - 1],
             v[:NUM_STATES, PROD_1, PROD_LEN_1, 0, :TOTAL_SIZE - 1],
             v[:NUM_STATES, PROD_2, PROD_LEN_2, 0, :TOTAL_SIZE - 1]])

    # print("DN \n", v[:NUM_STATES - 1, DN, DN, 0, :STOCK_SIZE - 1].round(2))
    # print("1 \n", v[:NUM_STATES - 1, PROD_1, PROD_LEN_1, 0, :STOCK_SIZE - 1].round(2))
    # print("2 \n", v[:NUM_STATES - 1, PROD_2, PROD_LEN_2, 0, :STOCK_SIZE - 1].round(2))

    action[:NUM_STATES, 0, 0, 0, :TOTAL_SIZE - 1] = \
        np.argmin([v[:NUM_STATES, DN, DN, 0, :TOTAL_SIZE - 1],
                   v[:NUM_STATES, PROD_1, PROD_LEN_1, 0, :TOTAL_SIZE - 1],
                   v[:NUM_STATES, PROD_2, PROD_LEN_2, 0, :TOTAL_SIZE - 1]],
                  axis=0)

    """
    If in the failed state or if the stock is at capacity do nothing.
    """
    action[NUM_STATES, 0, 0, 0, :TOTAL_SIZE] = DN
    action[:NUM_STATES, 0, 0, 0, TOTAL_SIZE - 1] = DN

    return u
