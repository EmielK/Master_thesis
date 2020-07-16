from .functions.TPM_gammaprocess import TPM_gammaprocess
from scipy.linalg import sqrtm

BACK_ORDER_COSTS = 0.01
STORAGE_COSTS = 0.003  # ~ BACK_ORDER_COSTS / 3

C_PM = 0.8
C_CM = 1

T_PM = 1
T_CM = 3

MAX_BACK_ORDER = 25
MAX_STORAGE = 10

COST_MISSED_ORDER = 1.2

NUM_STATES = 10
# No production, 1, and 2.
PROD_SETTINGS = 3

TIME_STEP_SIZE = 0.1
a = 2.5
a_1 = a
b_1 = 0.2
a_2 = a
b_2 = 0.5
# In the current state this only works correctly for a production length of 2
# for the slow production speed i.e. PROD_LEN_1 = 2.
PROB_MATRIX_1 = TPM_gammaprocess(a_1, b_1, 1, NUM_STATES, TIME_STEP_SIZE)
PROB_MATRIX_1 = sqrtm(PROB_MATRIX_1)
PROD_1 = 1
PROD_LEN_1 = 2
PROB_MATRIX_2 = TPM_gammaprocess(a_2, b_2, 1, NUM_STATES, TIME_STEP_SIZE)
PROD_2 = 2
PROD_LEN_2 = 1
# need one index extra since DN is also an option, for initialising array
MAX_PROD_TIME = PROD_LEN_1 + 1
MAX_MAIN_TIME = T_CM + 1
# + 1 since 0 is also an option
TOTAL_SIZE = MAX_BACK_ORDER + MAX_STORAGE + 1

DN = 0
MAINTENANCE = 1

PROB_NEW_JOBS = 0.3
MAX_NUM_NEW_JOBS = 3
PROB_1 = 1/2
PROB_2 = 1/3
PROB_3 = 1/6

# arbitrary large number
M = 10000
EPSILON = 0.0001
