import numpy as np

from MDP.constants import *


def new_job_arrival(v: np.ndarray) -> np.ndarray:
    """
    New job arrives in the system, which can happen in any system state. This
    only alters the stock value.
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
            # When neither production or maintenance is ongoing:
            u[:NUM_STATES + 1, 0, 0, 0, index] = \
                v[:NUM_STATES + 1, 0, 0, 0, index]
            # When production is ongoing:
            u[:NUM_STATES + 1, PROD_1, 1:, 0, index] = \
                v[:NUM_STATES + 1, PROD_1, 1:, 0, index]
            u[:NUM_STATES + 1, PROD_2, 1, 0, index] = \
                v[:NUM_STATES + 1, PROD_2, 1, 0, index]
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = v[0, 0, 0, 1:, index]
        elif index == 1:
            # When neither production or maintenance is ongoing:
            u[:NUM_STATES + 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * v[:NUM_STATES + 1, 0, 0, 0, index - 1]
            # When production is ongoing:
            u[:NUM_STATES + 1, PROD_1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, PROD_1, 1:, 0, index] \
                + PROB_NEW_JOBS * v[:NUM_STATES + 1, PROD_1, 1:, 0, index - 1]
            u[:NUM_STATES + 1, PROD_2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, PROD_2, 1, 0, index] \
                + PROB_NEW_JOBS * v[:NUM_STATES + 1, PROD_2, 1, 0, index - 1]
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * v[0, 0, 0, 1:, index - 1]
        elif index == 2:
            # When neither production or maintenance is ongoing:
            u[:NUM_STATES + 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (
                    PROB_1 * v[:NUM_STATES + 1, 0, 0, 0, index - 1] +
                    (PROB_2 + PROB_3) * v[:NUM_STATES + 1, 0, 0, 0, index - 2])
            # When production is ongoing:
            u[:NUM_STATES + 1, PROD_1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, PROD_1, 1:, 0, index] \
                + PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES + 1, PROD_1, 1:, 0, index - 1] +
                        (PROB_2 + PROB_3) *
                        v[:NUM_STATES + 1, PROD_1, 1:, 0, index - 2])
            u[:NUM_STATES + 1, PROD_2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, PROD_2, 1, 0, index] \
                + PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES + 1, PROD_2, 1, 0, index - 1] +
                        (PROB_2 + PROB_3) *
                        v[:NUM_STATES + 1, PROD_2, 1, 0, index - 2])
            # When maintenance is ongoing:
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * (
                    PROB_1 * v[0, 0, 0, 1:, index - 1] +
                    (PROB_2 + PROB_3) * v[0, 0, 0, 1:, index - 2])
        elif index >= 3:
            # When neither production or maintenance is ongoing:
            u[:NUM_STATES + 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES + 1, 0, 0, 0, index - 1] +
                        PROB_2 * v[:NUM_STATES + 1, 0, 0, 0, index - 2] +
                        PROB_3 * v[:NUM_STATES + 1, 0, 0, 0, index - 3])
            # When production is ongoing:
            u[:NUM_STATES + 1, PROD_1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, PROD_1, 1:, 0, index] \
                + PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES + 1, PROD_1, 1:, 0, index - 1] +
                        PROB_2 * v[:NUM_STATES + 1, PROD_1, 1:, 0, index - 2] +
                        PROB_3 * v[:NUM_STATES + 1, PROD_1, 1:, 0, index - 3])
            u[:NUM_STATES + 1, PROD_2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES + 1, PROD_2, 1, 0, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES + 1, PROD_2, 1, 0, index - 1] +
                        PROB_2 * v[:NUM_STATES + 1, PROD_2, 1, 0, index - 2] +
                        PROB_3 * v[:NUM_STATES + 1, PROD_2, 1, 0, index - 3])
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
