import numpy as np

from MDP.constants import *
from MDP.graph import graph
from MDP.subiterations.flow_cost import flow_cost
from MDP.subiterations.maintenance import maintenance
from MDP.subiterations.new_job_arrival import new_job_arrival
from MDP.subiterations.new_job_arrival_missed_cost \
    import new_job_arrival_missed_cost
from MDP.subiterations.new_production import new_production
from MDP.subiterations.transition_to_next_period import \
    transition_to_next_period
from MDP.functions import sensitivity_analysis, stock_analysis

np.set_printoptions(linewidth=400)


def main():
    """
    :return:
    """
    n = 0

    v0 = 0
    v = np.full(
        (1, NUM_STATES + 1, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME,
         TOTAL_SIZE)
        , v0
        , dtype="float")

    action_prod = np.full(
        (NUM_STATES + 1, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME,
         TOTAL_SIZE)
        , np.inf)

    action_maint = np.full(
        (NUM_STATES + 1, PROD_SETTINGS, MAX_PROD_TIME, MAX_MAIN_TIME,
         TOTAL_SIZE),
        np.inf)

    span = 2 * EPSILON

    while span > EPSILON:
        n += 1

        v_n = np.full(
            (1,
             NUM_STATES + 1,
             PROD_SETTINGS,
             MAX_PROD_TIME,
             MAX_MAIN_TIME,
             TOTAL_SIZE),
            np.NaN,
            dtype="float")
        v = np.concatenate((v, v_n), axis=0)

        u_3 = transition_to_next_period(v[n - 1, :, :, :, :, :])
        u_2 = new_production(u_3, action_prod)
        u_flow = flow_cost(u_2)
        u_1 = maintenance(u_flow, action_maint)
        if MAX_BACK_ORDER > 0:
            v[n, :, :, :, :, :] = new_job_arrival(u_1)
        else:
            v[n, :, :, :, :, :] = new_job_arrival_missed_cost(u_1)

        # print("transition to next period", '\n',
        #       u_3[:NUM_STATES + 1, 0, 0, 0, :].round(1))
        # print("new production", '\n', u_2[:NUM_STATES + 1, 0, 0, 0, :].round(1))
        # print("flow_cost", '\n', u_flow[:NUM_STATES + 1, 0, 0, 0, :].round(1))
        # print("maintenance", '\n', u_1[:NUM_STATES + 1, 0, 0, 0, :].round(1), '\n')
        # print("new_job \n ", v[n, :, 0, 0, 0, :].round(2), '\n')
        # print(v[n, :NUM_STATES + 1, 0, 0, 0, :].round(2) -
        #       v[n - 1, :NUM_STATES + 1, 0, 0, 0, :].round(2), '\n')

        max_it = np.nanmax((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        min_it = np.nanmin((v[n, :, :, :, :, :] - v[n - 1, :, :, :, :, :]))
        span = max_it - min_it
        cost_rate = (max_it + min_it) / (2 * TIME_STEP_SIZE)

        # if n == 100:
        #     break

        # print("min: ", min_it)
        # print("max: ", max_it)
        # print(span)

    print("iterations:", n)
    # If maintenance is the optimal action this overrides production if
    # production was the optimal action in the step prior so we must correct
    # for this.
    # print("production \n", action_prod[:NUM_STATES, 0, 0, 0, :], '\n')
    # print(v[n, :NUM_STATES + 1, 0, 0, 0, :].round(2), '\n')
    # print(v[n, :NUM_STATES, 0, 0, 0, :].round(2) -
    #       v[n - 1, :NUM_STATES, 0, 0, 0, :].round(2), '\n')
    # print("production \n", action_prod[:NUM_STATES + 1, 0, 0, 0, :], '\n')
    # print("maintenance \n", action_maint[:NUM_STATES + 1, 0, 0, 0, :], '\n')

    print("Cost rate: ", cost_rate)

    f = open("data/adding_stock", "a+")
    f.write(f"{MAX_STORAGE} {cost_rate}\n")
    f.close()

    graph(action_prod[:NUM_STATES, 0, 0, 0, :],
          action_maint[:NUM_STATES, 0, 0, 0, :])


if __name__ == "__main__":
    # main()
    # sensitivity_analysis()
    stock_analysis()
