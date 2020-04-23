import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from MDP.constants import *
from MDP.subiterations.maintenance import maintenance
from MDP.subiterations.new_job import new_job
from MDP.subiterations.new_production import new_production
from MDP.subiterations.transition_to_next_period import \
    transition_to_next_period


def main():
    """
    :return:
    """
    n = 0

    v0 = 0
    v = np.full(
        (1, NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME, STOCK_SIZE),
        v0)

    action_1 = np.full(
        (1, NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME, STOCK_SIZE),
        np.inf)

    action_2 = np.full(
        (1, NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME, STOCK_SIZE),
        np.inf)

    epsilon = 0.01
    span = 2 * epsilon

    while span > epsilon:
        n += 1

        v_n = np.full(
            (1,
             NUM_STATES,
             PROD_SETTINGS,
             MAX_PROD_TIME,
             MAX_MAIN_TIME,
             STOCK_SIZE),
            np.inf)
        v = np.concatenate((v, v_n), axis=0)

        action_1_n = np.full(
            (1,
             NUM_STATES,
             PROD_SETTINGS,
             MAX_PROD_TIME,
             MAX_MAIN_TIME,
             STOCK_SIZE),
            np.inf)
        action_1 = np.concatenate((action_1, action_1_n), axis=0)

        action_2_n = np.full(
            (1,
             NUM_STATES,
             PROD_SETTINGS,
             MAX_PROD_TIME,
             MAX_MAIN_TIME,
             STOCK_SIZE),
            np.inf)
        action_2 = np.concatenate((action_2, action_2_n), axis=0)

        transition_to_next_period(v, n)
        new_production(v, n, action_1)
        maintenance(v, n, action_2)
        new_job(v, n)

        max_it = np.amax((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        min_it = np.amin((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        span = max_it - min_it

    print(n)
    print(v[n, :, 0, 0, 0, :])
    print(action_1[n, :, 0, 0, 0, :])
    print(action_2[n, :, 0, 0, 0, :])


if __name__ == "__main__":
    main()
