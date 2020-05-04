import numpy as np

from MDP.constants import *


def new_job(v: np.ndarray) -> np.ndarray:
    """
    New job arrives in the system, which can happen in any system state. This
    only alters the stock value.
    """
    u = v.copy()

    for index in range(STOCK_SIZE):
        if index >= 3:
            # During maintenance
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * (PROB_1 * v[0, 0, 0, 1:, index - 1] +
                                 PROB_2 * v[0, 0, 0, 1:, index - 2] +
                                 PROB_3 * v[0, 0, 0, 1:, index - 3])
            # During prod setting 1
            u[:NUM_STATES - 1, 1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 1, 1:, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 1, 1:, 0, index - 1] +
                            PROB_2 * v[:NUM_STATES - 1, 1, 1:, 0, index - 2] +
                            PROB_3 * v[:NUM_STATES - 1, 1, 1:, 0, index - 3])
            # During prod setting 2
            u[:NUM_STATES - 1, 2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 2, 1, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 2, 1, 0, index - 1] +
                            PROB_2 * v[:NUM_STATES - 1, 2, 1, 0, index - 2] +
                            PROB_3 * v[:NUM_STATES - 1, 2, 1, 0, index - 3])
            # When neither production or maintenance is ongoing.
            u[:NUM_STATES - 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 0, 0, 0, index - 1] +
                            PROB_2 * v[:NUM_STATES - 1, 0, 0, 0, index - 2] +
                            PROB_3 * v[:NUM_STATES - 1, 0, 0, 0, index - 3])
        elif index == 2:
            # During maintenance
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * (PROB_1 * v[0, 0, 0, 1:, index - 1] +
                                 PROB_2 * v[0, 0, 0, 1:, index - 2] +
                                 PROB_3 * (v[0, 0, 0, 1:, index - 2] +
                                           COST_MISSED_ORDER))
            # During prod setting 1
            u[:NUM_STATES - 1, 1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 1, 1:, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 1, 1:, 0, index - 1] +
                            PROB_2 * v[:NUM_STATES - 1, 1, 1:, 0, index - 2] +
                            PROB_3 * (v[:NUM_STATES - 1, 1, 1:, 0, index - 2] +
                                      COST_MISSED_ORDER))
            # During prod setting 2
            u[:NUM_STATES - 1, 2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 2, 1, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 2, 1, 0, index - 1] +
                            PROB_2 * v[:NUM_STATES - 1, 2, 1, 0, index - 2] +
                            PROB_3 * (v[:NUM_STATES - 1, 2, 1, 0, index - 2] +
                                      COST_MISSED_ORDER))
            # When neither production or maintenance is ongoing.
            u[:NUM_STATES - 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 0, 0, 0, index - 1] +
                            PROB_2 * v[:NUM_STATES - 1, 0, 0, 0, index - 2] +
                            PROB_3 * (v[:NUM_STATES - 1, 0, 0, 0, index - 2] +
                                      COST_MISSED_ORDER))
        elif index == 1:
            # During maintenance
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * (PROB_1 * v[0, 0, 0, 1:, index - 1] +
                                 PROB_2 * (v[0, 0, 0, 1:, index - 1] +
                                           COST_MISSED_ORDER) +
                                 PROB_3 * (v[0, 0, 0, 1:, index - 1] +
                                           2 * COST_MISSED_ORDER))

            # During prod setting 1
            u[:NUM_STATES - 1, 1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 1, 1:, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 1, 1:, 0, index - 1] +
                            PROB_2 * (v[:NUM_STATES - 1, 1, 1:, 0, index - 1] +
                                      COST_MISSED_ORDER) +
                            PROB_3 * (v[:NUM_STATES - 1, 1, 1:, 0, index - 1] +
                                      2 * COST_MISSED_ORDER))
            # During prod setting 2
            u[:NUM_STATES - 1, 2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 2, 1, 0, index] + \
                PROB_NEW_JOBS * (
                            PROB_1 * v[:NUM_STATES - 1, 2, 1, 0, index - 1] +
                            PROB_2 * (v[:NUM_STATES - 1, 2, 1, 0, index - 1] +
                                      COST_MISSED_ORDER) +
                            PROB_3 * (v[:NUM_STATES - 1, 2, 1, 0, index - 1] +
                                      2 * COST_MISSED_ORDER))
            # When neither production or maintenance is ongoing.
            u[:NUM_STATES - 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (
                        PROB_1 * v[:NUM_STATES - 1, 0, 0, 0, index - 1] +
                        PROB_2 * (v[:NUM_STATES - 1, 0, 0, 0, index - 1] +
                                  COST_MISSED_ORDER) +
                        PROB_3 * (v[:NUM_STATES - 1, 0, 0, 0, index - 1] +
                                  2 * COST_MISSED_ORDER))

        elif index == 0:
            # During maintenance
            u[0, 0, 0, 1:, index] = \
                (1 - PROB_NEW_JOBS) * v[0, 0, 0, 1:, index] + \
                PROB_NEW_JOBS * (PROB_1 * (v[0, 0, 0, 1:, index] +
                                           COST_MISSED_ORDER) +
                                 PROB_2 * (v[0, 0, 0, 1:, index] +
                                           2 * COST_MISSED_ORDER) +
                                 PROB_3 * (v[0, 0, 0, 1:, index] +
                                           3 * COST_MISSED_ORDER))
            # During prod setting 1
            u[:NUM_STATES - 1, 1, 1:, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 1, 1:, 0, index] + \
                PROB_NEW_JOBS * (PROB_1 * (v[:NUM_STATES - 1, 1, 1:, 0, index] +
                                           COST_MISSED_ORDER) +
                                 PROB_2 * (v[:NUM_STATES - 1, 1, 1:, 0, index] +
                                           2 * COST_MISSED_ORDER) +
                                 PROB_3 * (v[:NUM_STATES - 1, 1, 1:, 0, index] +
                                           3 * COST_MISSED_ORDER))
            # During prod setting 2
            u[:NUM_STATES - 1, 2, 1, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 2, 1, 0, index] + \
                PROB_NEW_JOBS * (PROB_1 * (v[:NUM_STATES - 1, 2, 1, 0, index] +
                                           COST_MISSED_ORDER) +
                                 PROB_2 * (v[:NUM_STATES - 1, 2, 1, 0, index] +
                                           2 * COST_MISSED_ORDER) +
                                 PROB_3 * (v[:NUM_STATES - 1, 2, 1, 0, index] +
                                           3 * COST_MISSED_ORDER))
            # When neither production or maintenance is ongoing.
            u[:NUM_STATES - 1, 0, 0, 0, index] = \
                (1 - PROB_NEW_JOBS) * v[:NUM_STATES - 1, 0, 0, 0, index] + \
                PROB_NEW_JOBS * (PROB_1 * (v[:NUM_STATES - 1, 0, 0, 0, index] +
                                           COST_MISSED_ORDER) +
                                 PROB_2 * (v[:NUM_STATES - 1, 0, 0, 0, index] +
                                           2 * COST_MISSED_ORDER) +
                                 PROB_3 * (v[:NUM_STATES - 1, 0, 0, 0, index] +
                                           3 * COST_MISSED_ORDER))

    # print("new job", '\n', u[:NUM_STATES, 0, 0, 0, :].round(1), '\n')
    return u
