from scipy.fft import fft, fftfreq

def get_fft(data, fs):
    spectrum = (fft(data / (len(data) / 2)))[: len(data) // 2]
    freq_vec = fftfreq(len(data), 1 / fs)[: len(data) // 2]
    return spectrum, freq_vec
