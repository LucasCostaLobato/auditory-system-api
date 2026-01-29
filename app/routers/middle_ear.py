from fastapi import APIRouter, HTTPException, Query
import numpy as np
from typing import List, Optional

from app.models.middle_ear.deterministic_models import get_middle_ear_model
from app.models.outer_ear.outer_ear_functions import get_outer_ear_frf
from app.models.input_signal.input_signal_manager import input_signal_selector

router = APIRouter(prefix="/middle-ear", tags=["middleear"])


@router.get("/frf")
async def get_middle_ear_frf(
    fi: float,
    ff: float,
    nf: int,
    meCondition: Optional[str] = "healthy",
    meSeverity: Optional[str] = "low",
    measures: List[str] = Query(...),
):

    freq_vec, middle_ear_model = get_middle_ear_model(
        fi,
        ff,
        nf,
        meCondition,
        meSeverity,
    )


    output = {"freq_vec": freq_vec.tolist()}

    for measure in measures:
        output.update(
            {f"{measure}": (1000*np.abs(middle_ear_model[measure])).tolist()}
        )

    return output

@router.get("/dynamic-behavior")
async def get_middle_ear_dynamical_behavior(
    fi: float,
    ff: float,
    nf: int,
    ec_length: float,
    inputSignal: Optional[str] = "idealWhiteNoise",
    meCondition: Optional[str] = "healthy",
    meSeverity: Optional[str] = "low",
    measures: List[str] = Query(...),
):

    freq_vec, middle_ear_model = get_middle_ear_model(
        fi,
        ff,
        nf,
        meCondition,
        meSeverity,
    )

    input_position = 0
    output_position = ec_length
    
    x_vec = np.linspace(0,(ec_length / 1000),1000)

    oe_frf = get_outer_ear_frf(ec_length,input_position,output_position,freq_vec,x_vec,meCondition,meSeverity,False)
    input_signal = input_signal_selector[inputSignal](freq_vec)

    output = {"freq_vec": freq_vec.tolist()}

    for measure in measures:
        output.update(
            {f"{measure}": (np.abs(1000*middle_ear_model[measure]*oe_frf['frf']*input_signal)).tolist()}
        )

    return output