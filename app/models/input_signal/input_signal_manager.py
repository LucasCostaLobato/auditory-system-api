import json
import numpy as np

def get_ideal_white_noise(fi: float, ff: float, nf: int):

    freq_vec = np.linspace(fi, ff, nf)

    ideal_white_noise = np.ones(freq_vec.shape)

    return freq_vec, ideal_white_noise

def get_speech_signal(fi: float, ff: float, nf: int):

    freq_vec = np.linspace(fi, ff, nf)

    with open('app/database/speech_signal.json', 'r') as file:
        data = json.load(file)

    speech_signal = np.interp(freq_vec, data["freq"], data["data"])

    return freq_vec, speech_signal

input_signal_selector = {
    "idealWhiteNoise": get_ideal_white_noise,
    "speech": get_speech_signal
}
