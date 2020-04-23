import numpy as np

from ..constants import *


def transition_to_next_period(v: np.ndarray, n: int):
    """
    This function computes the new values after transitioning to the next
    period.
    """
    for index in range(STOCK_SIZE):
        if index < MAX_BACK_ORDER:
            cost_flow = -(index - MAX_BACK_ORDER) * BACK_ORDER_COSTS
        else:
            cost_flow = (index - MAX_BACK_ORDER) * STORAGE_COSTS

        # Do nothing i.e. Y = 0: maintenance
        for rep_time in range(MAX_MAIN_TIME - 1):
            v[n, :, 0, :, rep_time, index] = \
                v[n - 1, :, 0, :, rep_time + 1, index] + cost_flow

        # Production setting 1, i.e Y = 1, only for rem_rep_time = 0:
        for prod_time in range(MAX_PROD_TIME - 1):
            if index != 0:
                # TODO meerdere prob matrices dus eerste index geeft aan welke
                v[n, :, 1, prod_time, 0, index] = \
                    v[n - 1, :, 1, prod_time + 1, 0, index - 1].dot(
                        PROB_MATRIX_1 + cost_flow)
