

def get_sampling_rate(freq):

    if freq > 1000:
        return freq*3

    return freq * 10