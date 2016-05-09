#

import numpy as np
#from numpy import *


def beta_factor(max_win, link_cpdf, link_PRR):
    beta_factor = 0.0

    link_CW_meas = np.zeros((1, 2*max_win+1))
    link_CW_ind  = np.zeros((1, 2*max_win+1))

    for window in range(0, max_win):
        X0 = link_cpdf[max_win+1-window]
        X1 = link_cpdf[max_win+1+window]

        if X0 != 0:
            link_CW_meas[0][max_win + 1 - window] = X0
            link_CW_ind[0][max_win + 1 - window]  = link_PRR
            
        if X1 != 0:
            link_CW_meas[0][max_win + 1 + window] = (1.0 - X1)
            link_CW_ind[0][max_win + 1 + window]  = (1.0 - link_PRR)

    ############
    term1 = 0.0
    term2 = 0.0
    if any(link_CW_ind[0]):
        term1 = np.mean(link_CW_ind[0])

    if any(link_CW_meas[0]):
        term2 = np.mean(link_CW_meas[0])

    if term1 == 0 and term2 == 0:
        beta_factor = 0.0
    else:
        beta_factor = 1.0*(term1-term2)/term1

    return beta_factor

