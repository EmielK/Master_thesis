import numpy as np

from MDP.constants import *


def flow_cost(v: np.ndarray) -> np.ndarray:
    """
    Computes the flow cost for each index and adds it to the corresponding
     values.
    """
    u = v.copy()

    for index in range(STOCK_SIZE):
        if index < MAX_BACK_ORDER:
            cost_flow = (MAX_BACK_ORDER - index) * BACK_ORDER_COSTS
        else:
            cost_flow = (index - MAX_BACK_ORDER) * STORAGE_COSTS

        # During maintenance
        u[:, 0, 0, :, index] += cost_flow
        # During production setting 1, take care to account for correct length
        u[:NUM_STATES - 1, 1, 1:, 0, index] += cost_flow
        # During
        # u[:, :, 0, :, index] += cost_flow
        # print("During production \n", u[:, 1, 0, :, 2].round(2), '\n')

    return u
