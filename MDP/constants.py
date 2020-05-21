from .functions.TPM_gammaprocess import TPM_gammaprocess

BACK_ORDER_COSTS = 0.01
STORAGE_COSTS = 0.003  #BACK_ORDER_COSTS / 3

C_PM = 0.4
C_CM = 1

#   TODO not used atm
T_PM = 1
T_CM = 3

MAX_BACK_ORDER = 0
MAX_STORAGE = 15

# 15 is number of back-orders in model that considers both
test_value = sum(range(16))
COST_MISSED_ORDER = test_value * BACK_ORDER_COSTS

NUM_STATES = 9
# No production, 1, and 2.
PROD_SETTINGS = 3

TIME_STEP_SIZE = 0.1
PROB_MATRIX_1 = TPM_gammaprocess(5, 0.2, 1, NUM_STATES, TIME_STEP_SIZE)
PROD_1 = 1
PROD_LEN_1 = 2
PROB_MATRIX_2 = TPM_gammaprocess(7.5, 0.3, 1, NUM_STATES, TIME_STEP_SIZE)
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
PROB_1 = 0.5
PROB_2 = 1/3
PROB_3 = 1/6

# arbitrary large number
M = 10000
EPSILON = 0.00001
