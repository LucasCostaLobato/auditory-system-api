"""This module comprises the methods for modeling the human middle ear with deterministic approach"""
import numpy as np
from scipy.linalg import eigh
from typing import List, Optional

from app.models.middle_ear.utils import get_middle_ear_parameters

def get_mass_matrix(m1: float, m2: float, m3: float, m4: float) -> np.array:
    """This funtion returns the mass matrix of the lumped-element 
    model of the human middle ear, being:

    m1 the mass, in kg, of tympanic membrane
    m2 the mass, in kg, of malleus
    m3 the mass, in kg, of incus
    m4 the mass, in kg, of stapes
     
     
    For details, see https://doi.org/10.55753/aev.v35e52.34"""

    return np.matrix(np.diag([m1, m2, m3, m4]))


def get_stiffness_matrix(
    k1: float, k2: float, k3: float, k4: float, k5: float, k6: float, k7: float
) -> np.array:
    """This funtion returns the stiffness matrix of the lumped-element 
    model of the human middle ear, being:

    k1 the stiffness, in N/m, of tympanic membrane adna tympanic annulus
    k2 the stiffness, in N/m, of tympano-mallear connection (manubrium)
    k3 the stiffness, in N/m, of malleus ligaments and tensor-timpani tendon
    k4 the stiffness, in N/m, of incudomalleolar joint
    k5 the stiffness, in N/m, of incus ligaments
    k6 the stiffness, in N/m, of incudostapedial joint
    k7 the stiffness, in N/m, of stapes anullar ligament and stapedial tendon
     
    For details, see https://doi.org/10.55753/aev.v35e52.34"""

    l1 = [k1 + k2, -k2, 0, 0]
    l2 = [-k2, k2 + k3 + k4, -k4, 0]
    l3 = [0, -k4, k4 + k5 + k6, -k6]
    l4 = [0, 0, -k6, k6 + k7]

    return np.matrix([l1, l2, l3, l4])


def lumped_element_middle_ear_model(x: dict, freq: list, condition: str = "healthy", severity: str = "low") -> dict:
    """This function computes the modal solution of the deterministic model
    of the human middle ear, being:
    
    - x the mechanical parameters of middle ear according
    to function get_middle_ear_parameters()
    - freq is the frequency vector which the FRF will be defined
    - condition is the middle ear condition
    - severity is the severity of the middle ear conditions. If condition
    is 'healthy', severity is ignored 
     
    For details, see https://doi.org/10.55753/aev.v35e52.34"""

    if condition == "healthy":
        k7 = x["k7"]
        k3 = x["k3"]

    if condition == "otosclerosis":
        k3 = x["k3"]

        if severity == "low":
            k7 = x["k7"]*10
        if severity == "medium":
            k7 = x["k7"]*100
        if severity == "high":
            k7 = x["k7"]*1000

    if condition == "malFixation":
        k7 = x["k7"]

        if severity == "low":
            k3 = x["k3"]*10
        if severity == "medium":
            k3 = x["k3"]*100
        if severity == "high":
            k3 = x["k3"]*1000


    M = get_mass_matrix(x["m1"], x["m2"], x["m3"], x["m4"])
    K = get_stiffness_matrix(
        x["k1"], x["k2"], k3, x["k4"], x["k5"], x["k6"], k7
    )
    eta = [x["eta1"], x["eta2"], x["eta3"], x["eta4"]]
    tm_area = x["tmArea"]

    Zair = 343 * 1.21  # Characteristic air impedance
    P = 1  # Unitary pressure at tymapnic membrane
    F = np.matrix([P * tm_area, 0, 0, 0]).transpose()

    eigval, eigvec = eigh(K, M)

    omega_n = np.sqrt(np.real(eigval))
    natural_freq = omega_n / (2 * np.pi)

    # Deterministic modal matrices
    Mm = np.identity(len(omega_n))
    Km = np.diag(np.real(eigval))
    Cm = np.diag(eta * omega_n)

    # Modal excitation
    Fm = np.transpose(eigvec) * F

    # Auxiliar vectors to allocate results
    Hfp = list()
    Hmal = list()
    Hinc = list()
    Htm = list()
    Zme = list()
    ER = list()

    # Loop to compute the displacement FRF for each frequency bin
    for ind, f in enumerate(freq):
        angular_f = 2 * f * np.pi
        D = Km - angular_f ** 2 * Mm + 1j * angular_f * Cm
        Hm = np.linalg.inv(D)
        Xm = Hm * Fm  # Displacement in modal coordinates
        FRF = eigvec * Xm  # Displacement in physical coodinates

        Htm.append(1j * angular_f * FRF[0].item())
        Hmal.append(1j * angular_f * FRF[1].item())
        Hinc.append(1j * angular_f * FRF[2].item())
        Hfp.append(1j * angular_f * FRF[3].item())
        Zme.append(1 / (Htm[ind] * tm_area))
        ER.append((np.abs((Zme[ind] - Zair / tm_area) / (Zme[ind] + Zair / tm_area)) ** 2))

    return {
        "Htm": np.array(Htm),
        "Hmal": np.array(Hmal),
        "Hinc": np.array(Hinc),
        "Hfp": np.array(Hfp),
        "Zme": np.array(Zme),
        "ER": np.array(ER),
        "naturalFrequencies": natural_freq,
        "Km": np.matrix(Km),
        "Mm": np.matrix(Mm),
        "Cm": np.matrix(Cm),
        "Eigvec": np.matrix(eigvec)
    }


def get_middle_ear_model(
    fi: float,
    ff: float,
    nf: int,
    me_condition: Optional[str] = "healthy",
    me_severity: Optional[str] = "low"):

    if me_condition is None:
        me_condition = "healthy"
    if me_severity is None:
        me_severity = "low"

    freq_vec = np.linspace(fi, ff, nf)

    me_param = get_middle_ear_parameters("LVATB1")

    me_model = lumped_element_middle_ear_model(me_param,freq_vec,me_condition,me_severity)

    return freq_vec, me_model