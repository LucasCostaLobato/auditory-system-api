import numpy as np


def get_middle_ear_parameters(reference_parameter: str) -> dict:
    """This function returns the mechanical parameters of the middle ear
    from the fitting based on the reference_parameter.
     
    Possibles inputs:
        - "MerchantTB1_MultiObj" from http://dx.doi.org/10.1016/j.heares.2016.07.018
        - "LVATB1" from DOI: 10.17648/sobrac-87108
        - "Optimum_stochastic" from https://doi.org/10.1121/10.0009763
          
    For details, see https://doi.org/10.55753/aev.v35e52.34"""

    parameters = np.loadtxt(
        f"middle_ear/parameters/{reference_parameter}.txt", delimiter=" "
    )

    return {
        "m1": parameters[0],
        "m2": parameters[1],
        "m3": parameters[2],
        "m4": parameters[3],
        "k1": parameters[4],
        "k2": parameters[5],
        "k3": parameters[6],
        "k4": parameters[7],
        "k5": parameters[8],
        "k6": parameters[9],
        "k7": parameters[10],
        "eta1": parameters[11],
        "eta2": parameters[12],
        "eta3": parameters[13],
        "eta4": parameters[14],
        "tmArea": parameters[15],
    }
