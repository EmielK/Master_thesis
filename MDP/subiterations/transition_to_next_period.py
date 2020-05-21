import numpy as np

from ..constants import *


def transition_to_next_period(v: np.ndarray) -> np.ndarray:
    """
    This function computes the new values after transitioning to the next
    period. This needs to be done for every index since the flow costs depend
    on it.
    """
    u = np.full(
        (NUM_STATES + 1,
         PROD_SETTINGS,
         MAX_PROD_TIME,
         MAX_MAIN_TIME,
         TOTAL_SIZE),
        np.NaN,
        dtype="float")
    # Do nothing
    u[:NUM_STATES, 0, 0, 0, :] = v[:NUM_STATES, 0, 0, 0, :]

    # Continue with maintenance
    for maint_time in range(1, MAX_MAIN_TIME):
        u[0, 0, 0, maint_time, :] = \
            v[0, 0, 0, maint_time - 1, :]

    # Upon finishing with maintenance set state to as good as new i.e. 0.
    # u[0, 0, 0, 1, :] = v[0, 0, 0, 0, :]

    # Continue production with the same setting if the product does not
    # finish in this transition period and does not reach a failed state
    # plus value times the probability that the system does reach the
    # failed state.
    for index in range(TOTAL_SIZE - 1):
        for prod_time in range(2, MAX_PROD_TIME):
            cost_not_to_failure = \
                PROB_MATRIX_1[:NUM_STATES, :NUM_STATES].dot(
                    v[:NUM_STATES, PROD_1, prod_time - 1, 0, index])

            cost_to_failure = \
                PROB_MATRIX_1[:NUM_STATES, NUM_STATES].dot(
                    v[NUM_STATES, 0, 0, 0, index])

            u[:NUM_STATES, PROD_1, prod_time, 0, index] = \
                cost_not_to_failure + cost_to_failure

        # If the product would finish in this transition period.
        cost_not_to_failure = \
            PROB_MATRIX_1[:NUM_STATES, :NUM_STATES].dot(
                v[:NUM_STATES, 0, 0, 0, index + 1])

        cost_to_failure = \
            PROB_MATRIX_1[:NUM_STATES, NUM_STATES].dot(
                v[NUM_STATES, 0, 0, 0, index])

        u[:NUM_STATES, PROD_1, 1, 0, index] = \
            cost_not_to_failure + cost_to_failure

        # For setting 2 product would always finish in this transition period.
        cost_not_to_failure = \
            PROB_MATRIX_2[:NUM_STATES, :NUM_STATES].dot(
                v[:NUM_STATES, 0, 0, 0, index + 1])

        cost_to_failure = \
            PROB_MATRIX_2[:NUM_STATES, NUM_STATES].dot(
                v[NUM_STATES, 0, 0, 0, index])

        u[:NUM_STATES, PROD_2, 1, 0, index] = \
            cost_not_to_failure + cost_to_failure

    # print("1\n", u[:NUM_STATES - 1, PROD_1, 2, 0, :STOCK_SIZE - 1].round(1))
    # print("2\n", u[0, PROD_2, PROD_LEN_2, 0, :STOCK_SIZE - 1].round(1))

    return u
