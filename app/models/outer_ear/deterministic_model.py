import numpy as np

def eac_canal_acoustic_field(
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
