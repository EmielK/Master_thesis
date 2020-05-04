import numpy as np

from MDP.constants import *
from MDP.graph import graph
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

    action_prod = np.full(
        (NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME, STOCK_SIZE)
        , np.inf)

    action_maint = np.full(
        (NUM_STATES, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME,
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

        u_3 = transition_to_next_period(v[n - 1, :, :, :, :, :])
        u_2 = new_production(u_3, action_prod)
        u_flow = flow_cost(u_2)
        u_1 = maintenance(u_flow, action_maint)
        v[n, :, :, :, :, :] = new_job(u_1)

        print("v \n ", v[n, :, 0, 0, 0, :].round(2), '\n')

        max_it = np.amax((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        min_it = np.amin((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        span = max_it - min_it

        if n == 50:
            break

        print(span)

    # print(PROB_MATRIX_1.round(1))
    print("###########")
    print(max_it)
    print("###########")
    print(min_it)
    print("###########")
    print(n)
    # If maintenance is the optimal action this overrides production if
    # production was the optimal action in the step prior so we must correct
    # for this.
    # print("production \n", action_prod[:NUM_STATES, 0, 0, 0, :], '\n')
    print(v[n, :NUM_STATES, 0, 0, 0, :].round(2), '\n')
    # print(v[n, :NUM_STATES, 0, 0, 0, :].round(2) -
    #       v[n - 1, :NUM_STATES, 0, 0, 0, :].round(2), '\n')
    print("production \n", action_prod[:NUM_STATES, 0, 0, 0, :], '\n')
    print("maintenance \n", action_maint[:NUM_STATES, 0, 0, 0, :], '\n')

    # graph(action_prod[:NUM_STATES, 0, 0, 0, :],
    #       action_maint[:NUM_STATES, 0, 0, 0, :])


if __name__ == "__main__":
    # print(PROB_MATRIX_1.round(2))
    # print(PROB_MATRIX_2.round(2))
    main()
