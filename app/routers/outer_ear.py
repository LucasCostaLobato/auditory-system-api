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
    p_ref = 20*10**(-6) # reference pressure

    freq_vec, input_signal = input_signal_selector[inputSignal](fi,ff,nf)

    pressure, x_vec, freq_vec = get_eac_canal_acoustic_field(
        ec_length / 1000,
        fi,
        ff,
        nf,
        middleEarCondition,
        middleEarSeverity,
    )

    input_ind = np.argmin(abs(x_vec - 0))
    output_ind = [np.argmin(abs(x_vec - x / 1000)) for x in positions]

    output = {"freq_vec": freq_vec.tolist()}

    for index, ind_x in enumerate(output_ind):

        EC_FRF = np.abs(pressure[:,ind_x]/pressure[:,input_ind])

        pontual_pressure = np.abs(input_signal*EC_FRF)

        if level:
            output.update(
                {f"{positions[index]}": (20*np.log10(pontual_pressure/p_ref)).tolist()}
            )
        else:
            output.update(
                {f"{positions[index]}": pontual_pressure.tolist()}
            )

    #TODO: endpoint está muito demorado. Verificar gargalo.

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