import numpy as np

from ..constants import *


def maintenance(v: np.ndarray, n: int, action: np.ndarray):
    """
    Sets optimal values after planning maintenance.
    """
    # If in failed state maintenance is required.
    # After maintenance is scheduled state = 0, prod setting = 0 and remaining
    # prod time = 0.
    # TODO tel ik zo de period van geen production mee?
    for main_time in range(MAX_MAIN_TIME):
        v[n, NUM_STATES - 1, 0, :, main_time, :] = \
            v[n - 1, 0, 0, :, T_CM, :] + C_CM
        action[n, NUM_STATES - 1, 0, :, main_time, :] = MAINTENANCE

    # If maintenance is already being performed no new maintenance is planned.
    # (prod > 0 not possible when T > 0)
    # TODO moet ik hier ook voor Y>0 gelijk zetten etc?
    v[n, :, 0, :, 1:, :] = v[n - 1, :, 0, :, 1:, :]
    v[n, :, 0, :, 1:, :] = DN

    # In other cases choose cheapest option, maintenance vs no maintenance
    # So only at Y = T = L = 0
    for state in range(NUM_STATES - 1):
        v[n, state, 0, 0, 0, :] = \
            np.minimum(v[n - 1, state, 0, 0, DN, :],
                       v[n - 1, 0, 0, 0, T_PM, :] + C_PM)

        action[n, :NUM_STATES, 0, 0, 0, :] = \
            np.argmin([v[n - 1, state, 0, 0, DN, :],
                       v[n - 1, 0, 0, 0, T_PM, :] + C_PM],
                      axis=0)
