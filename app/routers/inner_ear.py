from fastapi import APIRouter
import numpy as np
from scipy.signal import hilbert

from app.models.inner_ear.basilar_membrane_model import BasilarMembraneModel, create_pure_tone
from app.models.inner_ear.utils import get_sampling_rate


router = APIRouter(prefix="/inner-ear", tags=["innerear"])


@router.get("/bm-travelling-waves")
async def get_basilar_membrane_travelling_waves(
    freq_stimulus: float,
):

    # Criar modelo
    bm = BasilarMembraneModel(n_sections=500)

    fs = 44100#get_sampling_rate(freq_stimulus)

    duration = 0.05

    # Simular tom de 1 kHz
    sound = create_pure_tone(freq_stimulus, duration=duration, fs=fs)

    _, displacement = bm.simulate_response(sound, fs, duration)

    extrapolated_displacement = displacement[::25,:]

    y = [(each_y*1e9).tolist() for each_y in extrapolated_displacement]

    output = {
        "x_vec": (1000*bm.x).tolist(),
        "displacement": y
    }
    return output


@router.get("/bm-envelope")
async def get_basilar_membrane_envelope(
    freq_stimulus: float,
):

    # Criar modelo
    bm = BasilarMembraneModel(n_sections=500)

    fs = get_sampling_rate(freq_stimulus)

    duration = 0.05

    # Simular tom de 1 kHz
    sound = create_pure_tone(freq_stimulus, duration=duration, fs=fs)

    _, displacement = bm.simulate_response(sound, fs, duration)

    envelope = np.abs(hilbert(displacement, axis=0))
    max_envelope = np.max(envelope, axis=0)

    output = {
        "x_vec": (1000*bm.x).tolist(),
        "envelope": (max_envelope/np.max(max_envelope)).tolist()
    }
    return output