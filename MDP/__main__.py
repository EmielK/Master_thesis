import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from MDP.constants import *
from MDP.subiterations.flow_cost import flow_cost
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
        (1, NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME, STOCK_SIZE)
        , v0
        , dtype="float")

    action_1 = np.full(
        (1, NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME, STOCK_SIZE)
        , np.inf)

    action_2 = np.full(
        (1, NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME,
         STOCK_SIZE),
        np.inf)

    epsilon = 0.001
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
            M,
            dtype="float")
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

        u_3 = transition_to_next_period(v[n - 1, :, :, :, :, :])
        u_2 = new_production(u_3, n, action_1)
        u_flow = flow_cost(u_2)
        u_1 = maintenance(u_flow, n, action_2)
        v[n, :, :, :, :, :] = new_job(u_1)

        # print("v \n ", v[n, :, 0, 0, 0, :].round(2), '\n')
        # print("During maintenance \n", v[n, :, 0, 0, :, 2].round(2), '\n')
        # print("During production \n", v[n, :, 1, :, 0, 2].round(2), '\n')
        print("Maintenance \n", v[n, :, 0, 0, :, 0].round(2))

        max_it = np.amax((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        min_it = np.amin((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        span = max_it - min_it

        print(span)
        # if n == 50:
        #     break

    # print(v)
    print(PROB_MATRIX_1.round(1))
    print("###########")
    print(max_it)
    print("###########")
    print(min_it)
    print("###########")
    print(n)
    print(v[n, :NUM_STATES, 0, 0, 0, :].round(2), '\n')
    print("production \n", action_1[n, :NUM_STATES, 0, 0, 0, :], '\n')
    print("maintenance \n", action_2[n, :NUM_STATES, 0, 0, 0, :], '\n')
    # print(action_1[n, :NUM_STATES, 0, 0, 0, :]
    #       + action_2[n, :NUM_STATES, 0, 0, 0, :])
    # print(PROB_MATRIX_1[:NUM_STATES - 1, NUM_STATES - 1])


if __name__ == "__main__":
    main()
