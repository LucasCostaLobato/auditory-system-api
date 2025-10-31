import numpy as np
from typing import List, Optional

from app.models.middle_ear.deterministic_models import lumped_element_middle_ear_model
from app.models.middle_ear.utils import get_middle_ear_parameters

def analytical_ear_canal_model(
    L: float,
    A: float,
    freq_vec: np.array,
    Zme: np.array,
    c0: float = 343,
    rho0: float = 1.21,
    u0: float = 1,
    eta: float = 0.08
):
    """This function returns the pressure field into the ear canal, being:
    
    - L the ear canal length, in m
    - A the area of ear canal cross section, in m^2
    - freq_vec the vector of frequencies to be analyzed, in Hz
    - Zme the complex middle ear input impedance, in N*s/m^3, defined for the same frequencies of freq_vec
    - c0 the sound speed, in m/s
    - rho0 the air density, in kg/m^3
    - u0 the input particle velocity at ear canal entrance
    - eta the acoustic damping, dimensionless"""

    P0 = u0*rho0*c0
    x_vec = np.linspace(0,L,1000)

    pressure = np.zeros((len(freq_vec),len(x_vec)), dtype=complex)
    velocity = np.zeros((len(freq_vec),len(x_vec)), dtype=complex)


    for ind_f, f in enumerate(freq_vec):
        Zme_norm = (Zme[ind_f]) / (-rho0 * c0)

        k = ((2 * np.pi * f) / c0) + 1j * eta * ((2 * np.pi * f) / c0)

        Psi = np.exp(1j*k*L) + np.exp(-1j*k*L) - Zme_norm*np.exp(1j*k*L) + Zme_norm*np.exp(-1j*k*L)
        A = (-P0*np.exp(-1j*k*L) - P0*Zme_norm*np.exp(-1j*k*L))/Psi
        B = P0 + A

        for ind_x, x in enumerate(x_vec):

            AA = A*np.exp(1j*k*x)
            BB = B*np.exp(-1j*k*x)
            
            pressure[ind_f,ind_x] = AA + BB
            velocity[ind_f,ind_x] = (AA - BB)/(rho0*c0)
    
    return pressure, velocity, x_vec


def get_eac_canal_acoustic_field(
    ec_length: float,
    fi: float,
    ff: float,
    nf: int,
    me_condition: Optional[str] = "healthy",
    me_severity: Optional[str] = "low",
):

    if me_condition is None:
        me_condition = "healthy"
    if me_severity is None:
        me_severity = "low"

    freq_vec = np.linspace(fi, ff, nf)

    me_param = get_middle_ear_parameters("LVATB1")

    middle_ear_model = lumped_element_middle_ear_model(
        me_param, freq_vec, me_condition, me_severity
    )

    pressure, _, x_vec = analytical_ear_canal_model(
        ec_length, me_param["tmArea"], freq_vec, middle_ear_model["Zme"]
    )

    return pressure, x_vec, freq_vec

