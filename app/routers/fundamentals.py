from typing import List

from fastapi import APIRouter, Query

from app.models.fundamentals.acoustics import get_sine_signal
from app.models.fundamentals.vibrations import get_one_dof


router = APIRouter(prefix="/fundamentals", tags=["fundamentals"])


@router.get("/acoustics")
async def get_acoustics_fundamentals(
    amplitudes: List[float] = Query(...),
    frequencies: List[float] = Query(...),
    phases: List[float] = Query(...),
):
    
    fs = 2000
    duration = 10

    signal, time, spectrum, freq_vec_fft = get_sine_signal(
        frequencies, amplitudes, phases, fs, duration
    )

    output = {
        "time": time.tolist(),
        "signal": signal.tolist(),
        "spectrum": spectrum.tolist(),
        "freq_vec": freq_vec_fft.tolist(),
    }

    return output


@router.get("/vibrations")
async def get_acoustics_fundamentals(k: List, m: List, c: List):

    frf, freq = get_one_dof(m, k, c)

    output = {"freq_vec": freq.tolist(), "frf": frf.tolist()}
    return output
