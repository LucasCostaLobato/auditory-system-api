from typing import List

import numpy as np
from scipy.signal import find_peaks

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
    space = np.linspace(0,343*duration,n_samples)
    
    signal_time = np.zeros(n_samples)
    signal_space = np.zeros(n_samples)

    c0 = 343

    for ind, freq in enumerate(frequencies):
        wave_number = (2*np.pi*freq)/c0

        signal_space = signal_space + amplitudes[ind]*np.sin(wave_number*space + np.deg2rad(phases[ind]))

        signal_time = signal_time + amplitudes[ind]*np.sin(2*np.pi*freq*time + np.deg2rad(phases[ind]))


    spectrum, freq_vec_fft = get_fft(signal_time, fs)

    # Optimize freq_vec limit
    peak_ind, _ = find_peaks(spectrum, height = np.mean(spectrum))
    last_freq_vec_ind = int(max(peak_ind)*2)

    return signal_space[:int(0.1*fs)+1], space[:int(0.1*fs)+1], signal_time[:int(0.1*fs)+1], time[:int(0.1*fs)+1], np.abs(spectrum[1:last_freq_vec_ind]), freq_vec_fft[1:last_freq_vec_ind]