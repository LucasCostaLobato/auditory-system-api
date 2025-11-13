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
):

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
    p_ref = 20*10**(-6) # reference pressure

    freq_vec, input_signal = input_signal_selector[inputSignal](fi,ff,nf)

    pressure, x_vec, freq_vec = get_eac_canal_acoustic_field(
        ec_length,
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