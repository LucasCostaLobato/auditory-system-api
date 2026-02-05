from typing import List

import numpy as np

def get_one_dof(m: float, k: float, c: float):

    freq = np.linspace(10,1000,300)
    omega = 2*np.pi*freq

    D = -(omega**2)*m + k + 1j*omega*c

    frf = np.linalg.inv(D)

    return np.abs(frf), freq