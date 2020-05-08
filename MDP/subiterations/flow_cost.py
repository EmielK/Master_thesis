import numpy as np

from MDP.constants import *


def flow_cost(v: np.ndarray) -> np.ndarray:
    """
    Computes the flow cost for each index and adds it to the corresponding
     values.
    Cannot be in failed state at this point.
    """
    u = np.full(
        (NUM_STATES + 1,
         PROD_SETTINGS,
         MAX_PROD_TIME,
         MAX_MAIN_TIME,
         TOTAL_SIZE),
        np.NaN,
        dtype="float")

    for index in range(TOTAL_SIZE):
        if index < MAX_BACK_ORDER:
            cost_flow = (MAX_BACK_ORDER - index) * BACK_ORDER_COSTS
        else:
            cost_flow = (index - MAX_BACK_ORDER) * STORAGE_COSTS
        # During maintenance, 1: for prod time since this is done below
        u[0, 0, 0, 1:, index] = v[0, 0, 0, 1:, index] + cost_flow
        # During production setting 1, take care to account for correct length
        u[:NUM_STATES, 1, 1:, 0, index] = \
            v[:NUM_STATES, 1, 1:, 0, index] + cost_flow
        # During production setting 2
        u[:NUM_STATES, 2, 1, 0, index] = \
            v[:NUM_STATES, 2, 1, 0, index] + cost_flow
        # When neither production or maintenance is ongoing.
        u[:NUM_STATES, 0, 0, 0, index] = \
            v[:NUM_STATES, 0, 0, 0, index] + cost_flow
        # print("During production \n", u[:, 1, 0, :, 2].round(2), '\n')
    # print("#", v[0, 0, 0, :, :])
    return u
