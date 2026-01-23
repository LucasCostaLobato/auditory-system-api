import json

import numpy as np
from scipy import signal

from app.models.utils import get_fft


def get_sweep_sine(sampling_rate: int, duration: float, fi: float, ff: float):

    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)


    return signal.chirp(t,fi,duration,ff)


def get_ideal_white_noise(freq_vec):

    ideal_white_noise = np.ones(freq_vec.shape)

    return ideal_white_noise


def get_speech_signal(freq_vec):

    with open('app/database/speech_signal.json', 'r') as file:
        data = json.load(file)

    speech_signal = np.interp(freq_vec, data["freq"], data["data"])

    return speech_signal



def get_clarinet_signal(freq_vec):

    with open('app/database/clarinet_signal.json', 'r') as file:
        data = json.load(file)

    clarinet_signal = np.interp(freq_vec, data["freq"], data["data"])

    return clarinet_signal


def get_narrow_band_signal_low_freq(freq_vec):

    sampling_rate = 2*freq_vec[-1]

    duration = 1/(freq_vec[2]-freq_vec[1])

    sweep = get_sweep_sine(sampling_rate, duration, freq_vec[0], freq_vec[-1])

    sos = signal.butter(10, [80,120], "bandpass", fs=sampling_rate, output="sos")
    filter_sweep = signal.sosfilt(sos, sweep)

    spectrum, freq_vec_fft = get_fft(filter_sweep, sampling_rate)

    normalized_spectrum = spectrum/np.max(spectrum)

    normalized_spectrum = np.interp(freq_vec, freq_vec_fft, normalized_spectrum)

    return normalized_spectrum
    

def get_narrow_band_signal_mid_freq(freq_vec):

    sampling_rate = 2*freq_vec[-1]

    duration = 1/(freq_vec[2]-freq_vec[1])

    sweep = get_sweep_sine(sampling_rate, duration, freq_vec[0], freq_vec[-1])

    sos = signal.butter(10, [800,1200], "bandpass", fs=sampling_rate, output="sos")
    filter_sweep = signal.sosfilt(sos, sweep)

    spectrum, freq_vec_fft = get_fft(filter_sweep, sampling_rate)

    normalized_spectrum = spectrum/np.max(spectrum)

    normalized_spectrum = np.interp(freq_vec, freq_vec_fft, normalized_spectrum)

    return normalized_spectrum


def get_narrow_band_signal_high_freq(freq_vec):

    sampling_rate = 2*freq_vec[-1]

    duration = 1/(freq_vec[2]-freq_vec[1])

    sweep = get_sweep_sine(sampling_rate, duration, freq_vec[0], freq_vec[-1])

    sos = signal.butter(10, [4800,5200], "bandpass", fs=sampling_rate, output="sos")
    filter_sweep = signal.sosfilt(sos, sweep)

    spectrum, freq_vec_fft = get_fft(filter_sweep, sampling_rate)

    normalized_spectrum = spectrum/np.max(spectrum)

    normalized_spectrum = np.interp(freq_vec, freq_vec_fft, normalized_spectrum)

    return normalized_spectrum
    

input_signal_selector = {
    "white_noise": get_ideal_white_noise,
    "speech": get_speech_signal,
    "clarinet": get_clarinet_signal,
    "narrowBandSignalLowFreq": get_narrow_band_signal_low_freq,
    "narrowBandSignalMidFreq": get_narrow_band_signal_mid_freq,
    "narrowBandSignalHighFreq": get_narrow_band_signal_high_freq
}
