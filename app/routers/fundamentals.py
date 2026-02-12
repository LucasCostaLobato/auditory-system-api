from typing import List

from fastapi import APIRouter, Query

from app.models.fundamentals.acoustics import get_sine_signal
from app.models.fundamentals.vibrations import get_one_dof

medium_manager = {"air": 343, "water": 1500}

router = APIRouter(prefix="/fundamentals", tags=["fundamentals"])


@router.get("/acoustics")
async def get_acoustics_fundamentals(
    medium: str,
    amplitudes: List[float] = Query(...),
    frequencies: List[float] = Query(...),
    phases: List[float] = Query(...),
):
    
    c0 = medium_manager[medium]
    fs = 15000
    duration = 10

    signal_space, space, signal_time, time, spectrum, freq_vec_fft = get_sine_signal(
        frequencies, amplitudes, phases, fs, duration, c0
    )

    output = {
        "signal_space": signal_space.tolist(),
        "space": space.tolist(),
        "signal_time": signal_time.tolist(),
        "time": time.tolist(),
        "spectrum": spectrum.tolist(),
        "freq_vec": freq_vec_fft.tolist(),
    }

    return output


@router.get("/vibrations")
async def get_vibration_fundamentals(stiffness: float, mass: float, damping: float):

    frf, freq = get_one_dof(mass, stiffness, damping)

    output = {"freq_vec": freq.tolist(), "frf": frf.tolist()}
    return output
