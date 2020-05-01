import numpy as np

from ..constants import *


def transition_to_next_period(v: np.ndarray) -> np.ndarray:
    """
    This function computes the new values after transitioning to the next
    period. This needs to be done for every index since the flow costs depend
    on it.
    """
    u = v.copy()
    # for index in range(STOCK_SIZE):
    #     if index < MAX_BACK_ORDER:
    #         cost_flow = (MAX_BACK_ORDER - index) * BACK_ORDER_COSTS
    #     else:
    #         cost_flow = (index - MAX_BACK_ORDER) * STORAGE_COSTS
        # test
        # u[:, :, :, :, index] = v[:, :, :, :, index] + cost_flow

        # Do nothing i.e. Y = L = T = 0
        # u[:, 0, 0, 0, index] = v[:, 0, 0, 0, index] + cost_flow

        # Continue with maintenance (old)
        # for maint_time in range(1, MAX_MAIN_TIME):
        #     u[0, 0, 0, maint_time, index] = \
        #         v[0, 0, 0, maint_time - 1, index] + cost_flow

    for maint_time in range(2, MAX_MAIN_TIME):
        u[0, 0, 0, maint_time, :] = \
            v[0, 0, 0, maint_time - 1, :]

    # Upon finishing with maintenance set state to as good as new i.e. 0.
    u[0, 0, 0, 1, :] = v[0, 0, 0, 0, :]

    # Continue production with the same setting if the product does not
    # finish in this transition period and does not reach a failed state
    # plus value times the probability that the system does reach the
    # failed state.
    # if index != STOCK_SIZE - 1:
    for index in range(STOCK_SIZE - 1):
        for prod_time in range(2, MAX_PROD_TIME):
            # print(PROB_MATRIX_1.round(1), '\n')
            # print(PROB_MATRIX_1[:NUM_STATES - 1, NUM_STATES - 1], '\n')
            # print(v[NUM_STATES - 1, 0, 0, 0, :STOCK_SIZE - 1])
            # TODO meerdere prob matrices toevoegen
            u[:NUM_STATES - 1, PROD_1, prod_time, 0, index] = \
                PROB_MATRIX_1[:NUM_STATES - 1, :NUM_STATES - 1].dot(
                    v[:NUM_STATES - 1, PROD_1, prod_time - 1, 0, index])\
                + \
                PROB_MATRIX_1[:NUM_STATES - 1, NUM_STATES - 1].dot(
                    v[NUM_STATES - 1, 0, 0, 0, index])
        # TODO ik zet niet meer de state meteen op 1 misschien nog doen?
        # If the product would finish in this transition period.
        # for index in range(STOCK_SIZE - 1):
        u[:NUM_STATES - 1, PROD_1, 1, 0, index] = \
            PROB_MATRIX_1[:NUM_STATES - 1, :NUM_STATES - 1].dot(
                v[:NUM_STATES - 1, 0, 0, 0, index + 1]) + \
            PROB_MATRIX_1[:NUM_STATES - 1, NUM_STATES - 1].dot(
                v[NUM_STATES - 1, 0, 0, 0, index])

    # print("transition to next period", '\n', u[:NUM_STATES, 0, 0, 0, :].round(1)
    #       , '\n')
    return u
