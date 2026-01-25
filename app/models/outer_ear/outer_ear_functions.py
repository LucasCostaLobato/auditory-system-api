import numpy as np

from app.models.outer_ear.deterministic_model import get_eac_canal_acoustic_field

def get_outer_ear_frf(
    ec_length, 
    input_position, 
    output_position,
    freq_vec, 
    x_vec,
    meCondition,
    meSeverity,
    level):


    pressure = get_eac_canal_acoustic_field(
        ec_length / 1000,
        freq_vec,
        x_vec,
        meCondition,
        meSeverity,
    )

    input_ind = np.argmin(abs(x_vec - input_position))
    output_ind = np.argmin(abs(x_vec - output_position))
    
    EC_FRF = np.abs(pressure[:,output_ind]/pressure[:,input_ind])

    output = {"freq_vec": freq_vec.tolist()}

    if level:
        output.update(
            {f"frf": (20*np.log10(np.abs(EC_FRF))).tolist()}
        )
    else:
        output.update(
            {f"frf": np.abs(EC_FRF).tolist()}
        )

    return output