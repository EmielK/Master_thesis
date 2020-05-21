import numpy as np

from ..constants import *


def maintenance(v: np.ndarray, action: np.ndarray) -> np.ndarray:
    """
    Adds the costs of maintenance.
    If the system is in the failed state maintenance is mandatory and
    corrective maintenance costs are incurred. Otherwise when there is no
    ongoing maintenance or production the cost minimizing option, maintenance
    versus doing nothing, is computed and selected.
    """
    u = np.full(
        (NUM_STATES + 1,
         PROD_SETTINGS,
         MAX_PROD_TIME,
         MAX_MAIN_TIME,
         TOTAL_SIZE),
        np.NaN,
        dtype="float")

    """
    If the system is in the failed state maintenance is required. After 
    maintenance is scheduled state = 0, prod setting = 0 and remaining
    prod time = 0, the remaining maintenance time is T_CM.
    When the system entered the failed state Y has been set to 0 in 
    transition_to_next_period.
    """
    # During maintenance:
    u[0, 0, 0, 1:, :] = v[0, 0, 0, 1:, :]

    # During production:
    u[:NUM_STATES, PROD_1, 1:, 0, :] = v[:NUM_STATES, PROD_1, 1:, 0, :]
    u[:NUM_STATES, PROD_2, 1, 0, :] = v[:NUM_STATES, PROD_2, 1, 0, :]

    # If in failed state
    u[NUM_STATES, 0, 0, 0, :] = v[0, 0, 0, T_CM, :] + C_CM
    action[NUM_STATES, 0, 0, 0, :] = MAINTENANCE

    """
    If there is no ongoing maintenance or production, so Y = T = L = 0, choose
    the cheapest option, where the options are do nothing and perform 
    maintenance.
    """
    for state in range(NUM_STATES):
        u[state, 0, 0, 0, :] = \
            np.minimum(v[state, 0, 0, 0, :],
                       v[0, 0, 0, T_PM, :] + C_PM)

        action[state, 0, 0, 0, :] = \
            np.argmin([v[state, 0, 0, 0, :],
                       v[0, 0, 0, T_PM, :] + C_PM],
                      axis=0)

    # print("DN: \n", v[:, 0, 0, 0, :].round(10))
    # print("M: \n", v[0, 0, 0, T_PM, :].round(10) + C_PM)
    return u
