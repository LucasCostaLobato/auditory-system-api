from typing import List

import numpy as np

def get_one_dof(m: float, k: float, c: float):
    '''
    This function returns the displacement FRF, in um/N, of 1 degree of freedom
    system, being
    - m the mass in kg,
    - k the stiffness in kN/m
    - c the damping in Ns/m
    '''

    freq = np.linspace(10,1000,300)
    omega = 2*np.pi*freq

    D = -(omega**2)*m + (k*1000) + 1j*omega*c

    frf = 1/D

    return 1000000*np.abs(frf[1:]), freq[1:]