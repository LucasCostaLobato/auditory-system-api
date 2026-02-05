from typing import List

import numpy as np

from app.models.utils import get_fft


def get_sine_signal(frequencies: List, amplitudes: List, phases: List, fs: int, duration: float):
    '''
    This function returns the sum of sine functions according to the lists
    - frequencies: frequencies in Hz
    - amplitudes: amplitudes, dimensionless
    - phases: phases, in degree
    - fs: sampling rate, in Hz
    - duration: total tima duration of the signal, in seconds
    '''

    n_samples = int(fs*duration)
    time = np.linspace(0,duration,n_samples)
    signal = np.zeros(n_samples)


    for ind, freq in enumerate(frequencies):
        signal = signal + amplitudes[ind]*np.sin(2*np.pi*freq*time + np.deg2rad(phases[ind]))


    spectrum, freq_vec_fft = get_fft(signal, fs)


    return signal[:int(0.1*fs)+1], time[:int(0.1*fs)+1], np.abs(spectrum[1:]), freq_vec_fft[1:]