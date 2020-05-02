import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.integrate as integrate
from scipy.stats import gamma

from MDP.constants import NUM_STATES, STOCK_SIZE


def graph(actions_1: np.ndarray, actions_2: np.ndarray):
    """
    heatmap x coordinates start at 0 so an extra row and column are added and
    left out in the figure. The graph works for nr_units = 2 only
    """
    # TODO Good as new state 0 should be 1 in paper.
    # TODO better difference between maintenance and production.
    actions = actions_1 + actions_2

    solution = actions

    extra_column = np.zeros((NUM_STATES + 1, 1))
    extra_row = np.zeros((1, STOCK_SIZE))
    solution = np.column_stack((extra_column, solution))
    solution = np.row_stack((extra_row, solution))

    ax = sns.heatmap(solution, square=True, linecolor='Black', cbar=False,
                     linewidths=0.1, cmap="Greys")

    # fix for mpl bug that cuts off top/bottom of seaborn viz
    b, t = plt.ylim()  # discover the values for bottom and top
    b += 0.5
    t -= 0.5
    plt.ylim(b, t)  # update the ylim(bottom, top) values
    plt.xlabel("Stock")
    plt.ylabel("State")
    ax.xaxis.tick_top()  # x axis on top
    ax.xaxis.set_label_position('top')
    plt.xlim(0, 12)
    plt.ylim(12, 0)
    plt.savefig('DecisionMatrix.pdf')
    plt.show()
