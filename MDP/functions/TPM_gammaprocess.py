import numpy as np
import scipy.integrate as integrate
from scipy.stats import gamma


def TPM_gammaprocess(a, b, L, m, dt):
    """
    Discretize a gamma deterioration process for a stationary gamma
    deterioration process.

    :param a: shape parameter for the gamma distribution
    :param b: scale parameter for the gamma distribution
    :param L: threshold level
    :param m: number of states in the discrete Markov process
    :param dt: discretized increments of time
    :return:
    """

    P = np.zeros((m + 1,  m + 1))

    dx = L / m

    def prob(i, dx, dt, a, b):
        return (1 / dx) * integrate.quad(
            lambda x: gamma.cdf(x, a=a * dt, scale=b), i * dx, (i + 1) * dx)[0]

    vprob = [0] * len(P)

    for idx in range(len(P)):
        vprob[idx] = prob(idx, dx, dt, a, b)

    p = np.diff(vprob, prepend=0)

    for idx in range(len(P)):
        P[idx, idx:m] = p[0:(m - idx)]
        P[idx, m] = 1 - sum(P[idx, 0:-1])

    return P
