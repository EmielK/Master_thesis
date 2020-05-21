import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.integrate as integrate
from scipy.stats import gamma

from MDP.constants import NUM_STATES, TOTAL_SIZE, MAX_BACK_ORDER, MAX_STORAGE


def graph(actions_1: np.ndarray, actions_2: np.ndarray):
    """
    heatmap x coordinates start at 0 so an extra row and column are added and
    left out in the figure.

    Assumes actions_2 is maintenance which overrides production (action_1).
    """
    # TODO better difference between maintenance and production.
    actions = actions_1

    actions[actions_2 == 1] = 3

    solution = actions

    print(solution)

    extra_column = np.zeros((NUM_STATES, 1))
    extra_row = np.zeros((1, TOTAL_SIZE + 1))
    solution = np.column_stack((extra_column, solution))
    solution = np.row_stack((extra_row, solution))

    ax = sns.heatmap(solution, square=False, linecolor='Black', cbar=False,
                     linewidths=0.1, cmap="Greys")

    # fix for mpl bug that cuts off top/bottom of seaborn viz
    b, t = plt.ylim()  # discover the values for bottom and top
    b += 0.5
    t -= 0.5
    plt.ylim(b, t)  # update the ylim(bottom, top) values
    plt.xlabel("Backorder index / Stock index")
    plt.ylabel("State")
    ax.xaxis.tick_top()  # x axis on top
    xlabel = range(-(MAX_BACK_ORDER + 1), MAX_STORAGE + 1)
    ax.set_xticklabels(xlabel)
    ax.xaxis.set_label_position('top')
    plt.xlim(1, TOTAL_SIZE + 1)
    plt.ylim(NUM_STATES + 2, 1)
    plt.savefig('DecisionMatrix.pdf')
    plt.show()
