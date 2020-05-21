import numpy as np

from MDP.constants import *


def new_job_arrival_missed_cost(v: np.ndarray) -> np.ndarray:
    """
    New job arrives in the system, which can happen in any system state. This
    only alters the stock value.
    Includes the failed state since this occurs before maintenance takes place,
    which set the failed state to as good as new.

    Includes missed cost.
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
        if index == 0:
            missed_cost = PROB_NEW_JOBS * (PROB_1 + 2 * PROB_2 + 3 * PROB_3) * \
                          COST_MISSED_ORDER
            # When neither production or maintenance is ongoing:
            u[:, 0, 0, 0, index] = \
                v[:, 0, 0, 0, index] + missed_cost
            # When production is ongoing:
            u[:NUM_STATES, PROD_1, 1:, 0, index] = \
                v[:NUM_STATES, PROD_1, 1:, 0, index] + missed_cost
            u[:NUM_STATES, PROD_2, 1, 0, index] = \
                v[:NUM_STATES, PROD_2, 1, 0, index] + missed_cost
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = v[0, 0, 0, 1:, index] + missed_cost
        elif index == 1:
            missed_cost = PROB_NEW_JOBS * (1 * PROB_2 + 2 * PROB_3) * \
                          COST_MISSED_ORDER
            # When neither production or maintenance is ongoing:
            u[:, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:, 0, 0, 0, index] + \
                PROB_NEW_JOBS * v[:, 0, 0, 0, index - 1] + \
                missed_cost
            # When production is ongoing:
            u[:NUM_STATES, PROD_1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES, PROD_1, 1:, 0, index] \
                + PROB_NEW_JOBS * v[:NUM_STATES, PROD_1, 1:, 0, index - 1] + \
                missed_cost
            u[:NUM_STATES, PROD_2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES, PROD_2, 1, 0, index] \
                + PROB_NEW_JOBS * v[:NUM_STATES, PROD_2, 1, 0, index - 1] + \
                missed_cost
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * v[0, 0, 0, 1:, index - 1] + \
                missed_cost
        elif index == 2:
            missed_cost = PROB_NEW_JOBS * (1 * PROB_3) * \
                          COST_MISSED_ORDER
            # When neither production or maintenance is ongoing:
            u[:, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:, 0, 0, 0, index] + \
                PROB_NEW_JOBS * \
                (
                        PROB_1 * v[:, 0, 0, 0, index - 1] +
                        (PROB_2 + PROB_3) * v[:, 0, 0, 0, index - 2]
                ) + missed_cost
            # When production is ongoing:
            u[:NUM_STATES, PROD_1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES, PROD_1, 1:, 0, index] \
                + PROB_NEW_JOBS * \
                (
                        PROB_1 * v[:NUM_STATES, PROD_1, 1:, 0, index - 1] +
                        (PROB_2 + PROB_3) *
                        v[:NUM_STATES, PROD_1, 1:, 0, index - 2]
                ) + missed_cost
            u[:NUM_STATES, PROD_2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES, PROD_2, 1, 0, index] \
                + PROB_NEW_JOBS * \
                (
                        PROB_1 * v[:NUM_STATES, PROD_2, 1, 0, index - 1] +
                        (PROB_2 + PROB_3) *
                        v[:NUM_STATES, PROD_2, 1, 0, index - 2]
                ) + missed_cost
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * \
                (
                    PROB_1 * v[0, 0, 0, 1:, index - 1] +
                    (PROB_2 + PROB_3) * v[0, 0, 0, 1:, index - 2]
                ) + missed_cost
        elif index >= 3:
            # When neither production or maintenance is ongoing:
            u[:, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[:, 0, 0, 0, index - 1] +
                        PROB_2 * v[:, 0, 0, 0, index - 2] +
                        PROB_3 * v[:, 0, 0, 0, index - 3])
            # When production is ongoing:
            u[:NUM_STATES, PROD_1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES, PROD_1, 1:, 0, index] \
                + PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES, PROD_1, 1:, 0, index - 1] +
                        PROB_2 * v[:NUM_STATES, PROD_1, 1:, 0, index - 2] +
                        PROB_3 * v[:NUM_STATES, PROD_1, 1:, 0, index - 3])
            u[:NUM_STATES, PROD_2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES, PROD_2, 1, 0, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES, PROD_2, 1, 0, index - 1] +
                        PROB_2 * v[:NUM_STATES, PROD_2, 1, 0, index - 2] +
                        PROB_3 * v[:NUM_STATES, PROD_2, 1, 0, index - 3])
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[0, 0, 0, 1:, index - 1] +
                        PROB_2 * v[0, 0, 0, 1:, index - 2] +
                        PROB_3 * v[0, 0, 0, 1:, index - 3])
        else:
            print("error for index: ", index)
            breakpoint()

    return u
