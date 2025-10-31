import numpy as np


def get_ideal_white_noise(
    fi: float,
    ff: float,
    nf: int):


    freq_vec = np.linspace(fi, ff, nf)

    ideal_white_noise = np.ones(freq_vec.shape)

    return freq_vec, ideal_white_noise

input_signal_selector = {
    "idealWhiteNoise": get_ideal_white_noise
}
