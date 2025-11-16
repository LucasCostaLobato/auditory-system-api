from typing import List, Optional

import numpy as np
from fastapi import APIRouter, HTTPException, Query

from app.models.input_signal.input_signal_manager import input_signal_selector
from app.models.outer_ear.deterministic_model import get_eac_canal_acoustic_field

router = APIRouter(prefix="/outer-ear", tags=["outerear"])


@router.get("/space-domain-analysis")
async def get_outer_ear_space_domain_analysis(
    ec_length: float,
    fi: float,
    ff: float,
    nf: int,
    frequencies: List[float] = Query(...),
    me_condition: Optional[str] = "healthy",
    me_severity: Optional[str] = "low",
    inputSignal: Optional[str] = "idealWhiteNoise",
):
    '''
    This endpoint return the pressure in the ear canal length domain for a given list
    of "frequencies", being:
     - ec_length the ear canal lenth, in mm (milimeters);
     - fi the initial frequency, in Hz;
     - ff the final frequency, in Hz;
     - nf, number of frequencies, dimensionless;
     - frequencies, the frequencies to be analyzed, in mm (milimeters);
     - middleEarCondition, the condition of the middle ear: "healty", 
     "otosclerosis", "malFixation";
     - middleEarSeverity, the severity of the middle ear condition (ignored if 
     middleEarCondition is "healthy): "low", "medium", "high";
     - inputSignal, the input signal at the ear canal entrance (see input_signal_selector
     to check the options).
    '''

    # x_vec = np.linspace(0,(ec_length / 1000),1000)
    pressure, x_vec, freq_vec = get_eac_canal_acoustic_field(
        ec_length,
        fi,
        ff,
        nf,
        me_condition,
        me_severity,
    )

    ind_freqs = [np.argmin(abs(freq_vec - f)) for f in frequencies]

    output = {"x_vec": x_vec.tolist()}

    for index, ind_freq in enumerate(ind_freqs):
        output.update(
            {f"{frequencies[index]}": np.real(pressure[ind_freq, :]).tolist()}
        )

    #TODO: basear endpoint na FRF para poder usar inputSignal

    return output

@router.get("/frequency-domain-analysis")
async def get_outer_ear_frequency_domain_analysis(
    ec_length: float,
    fi: float,
    ff: float,
    nf: int,
    positions: List[float] = Query(...),
    middleEarCondition: Optional[str] = "healthy",
    middleEarSeverity: Optional[str] = "low",
    inputSignal: Optional[str] = "idealWhiteNoise",
    level: Optional[bool] = True,
):
    '''
    This endpoint return the pressure in the frequency domain at given "positions",
    being:
     - ec_length the ear canal lenth, in mm (milimeters);
     - fi the initial frequency, in Hz;
     - ff the final frequency, in Hz;
     - nf, number of frequencies, dimensionless;
     - positions, the positions from the ear canal entrance to be analyzed, in 
     mm (milimeters);
     - middleEarCondition, the condition of the middle ear: "healty", 
     "otosclerosis", "malFixation";
     - middleEarSeverity, the severity of the middle ear condition (ignored if 
     middleEarCondition is "healthy): "low", "medium", "high";
     - inputSignal, the input signal at the ear canal entrance (see input_signal_selector
     to check the options);
     - level, a boolean to define the output unit. If True, the Sound Pressure Level, in dB SPL
     is returned.
    '''
    # Reference pressure
    p_ref = 20*10**(-6) 

    # Getting the input signal
    freq_vec, input_signal = input_signal_selector[inputSignal](fi,ff,nf)

    # Builing the space and frequency vectors
    x_vec =[each_position / 1000 for each_position in positions]
    freq_vec = np.linspace(fi, ff, nf)

    # Adding 0 position (ear canal entrance in the case the user did not request
    # It is needed to compute the FRF considering the input signal at ear canal entrance (x=0)
    if 0 in positions:
        x_vec = np.array(x_vec)
    else:
        x_vec.insert(0,0)
        x_vec = np.array(x_vec)

    # Computing the pressure along the ear canal 
    pressure = get_eac_canal_acoustic_field(
        ec_length / 1000,
        freq_vec,
        x_vec,
        middleEarCondition,
        middleEarSeverity,
    )

    output = {"freq_vec": freq_vec.tolist()}
    
    for ind_x, each_position in enumerate(positions):

        # If user did not requested position 0, skip the pressure at 0
        if 0 not in positions:
            ind_x = ind_x + 1

        # Compute the FRF between the ear canal entrance and "each_position"
        EC_FRF = np.abs(pressure[:,ind_x]/pressure[:,0])

        # Computing the pressure considering the input_signal at ear canal entrance 
        pontual_pressure = np.abs(input_signal*EC_FRF)

        if level:
            output.update(
                {f"{each_position}": (20*np.log10(pontual_pressure/p_ref)).tolist()}
            )
        else:
            output.update(
                {f"{each_position}": pontual_pressure.tolist()}
            )

    return output

@router.get("/frf")
async def get_outer_ear_frf(
    ec_length: float,
    fi: float,
    ff: float,
    nf: int,
    input_position: float,
    output_position: float,
    me_condition: Optional[str] = "healthy",
    me_severity: Optional[str] = "low",
    level: Optional[bool] = True,
):

    pressure, x_vec, freq_vec = get_eac_canal_acoustic_field(
        ec_length,
        fi,
        ff,
        nf,
        me_condition,
        me_severity,
    )

    input_ind = np.argmin(abs(x_vec - input_position))
    output_ind = np.argmin(abs(x_vec - output_position))
    
    EC_FRF = np.abs(pressure[:,output_ind]/pressure[:,input_ind])

    output = {"freq_vec": freq_vec.tolist()}

    if level:
        output.update(
            {f"frf": (20*np.log10(np.abs(EC_FRF))).tolist()}
        )
    else:
        output.update(
            {f"frf": np.abs(EC_FRF).tolist()}
        )

    return output