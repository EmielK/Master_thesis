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

        u[:, :, :, :, index] += cost_flow

    return u
