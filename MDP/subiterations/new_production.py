import numpy as np

from ..constants import *


def new_production(v: np.ndarray, action: np.ndarray) -> np.ndarray:
    """
    Computes the optimal choice regarding whether to start a new production
    cycle or not and assigns this value this value to the value array.
    """

    u = np.full(
        (NUM_STATES + 1,
         PROD_SETTINGS,
         MAX_PROD_TIME,
         MAX_MAIN_TIME,
         TOTAL_SIZE),
        np.NaN,
        dtype="float")

    # During maintenance:
    u[0, 0, 0, 1:, :] = v[0, 0, 0, 1:, :]

    # If production is still ongoing:
    u[:, PROD_1, 1:, 0, :] = v[:, PROD_1, 1:, 0, :]

    # If in the failed state or if the stock is at capacity do nothing.
    # failed state cannot actually occur here.
    # u[NUM_STATES, 0, 0, 0, :TOTAL_SIZE] = v[NUM_STATES, 0, 0, 0, :TOTAL_SIZE]
    action[NUM_STATES, 0, 0, 0, :TOTAL_SIZE] = DN

    u[:NUM_STATES, 0, 0, 0, TOTAL_SIZE - 1] =\
        v[:NUM_STATES, 0, 0, 0, TOTAL_SIZE - 1]
    action[:NUM_STATES, 0, 0, 0, TOTAL_SIZE - 1] = DN

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

    # print("DN \n", v[82:84, DN, DN, 0, 30].round(10))
    # print("1 \n", v[82:84, PROD_1, PROD_LEN_1, 0, 30].round(10))
    # print("2 \n", v[82:84, PROD_2, PROD_LEN_2, 0, 30].round(10))

    action[:NUM_STATES, 0, 0, 0, :TOTAL_SIZE - 1] = \
        np.argmin([v[:NUM_STATES, DN, DN, 0, :TOTAL_SIZE - 1],
                   v[:NUM_STATES, PROD_1, PROD_LEN_1, 0, :TOTAL_SIZE - 1],
                   v[:NUM_STATES, PROD_2, PROD_LEN_2, 0, :TOTAL_SIZE - 1]],
                  axis=0)

    return u
