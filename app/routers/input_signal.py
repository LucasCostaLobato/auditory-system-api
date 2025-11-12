from fastapi import APIRouter, HTTPException, Query
import numpy as np
from typing import List, Optional

from app.models.input_signal.input_signal_manager import input_signal_selector

router = APIRouter(prefix="/input-signal", tags=["inputsignal"])


@router.get("/magnitude-spectrum")
async def get_input_signal_magnitude_spectrum(
    fi: float,
    ff: float,
    nf: int,
    inputSignal: Optional[str] = "idealWhiteNoise",
    level: Optional[bool] = True,
):
    
    p_ref = 20*10**(-6) # reference pressure

    freq_vec, input_signal = input_signal_selector[inputSignal](fi,ff,nf)

    if level:
        amplitude = 20*np.log10(np.abs(input_signal)/p_ref)
    else:
        amplitude = np.abs(input_signal)

    output = {"freq_vec": freq_vec.tolist(), "magnitude": amplitude.tolist()}

    return output