from fastapi import APIRouter, HTTPException,Query
import numpy as np
from typing import List, Optional

from app.models.outer_ear.deterministic_model import eac_canal_acoustic_field
from app.models.middle_ear.deterministic_models import get_middle_ear_model
from app.models.middle_ear.utils import get_middle_ear_parameters

router = APIRouter(
    prefix="/outer-ear",
    tags=["outerear"]
)


@router.get("/space-domain-analysis")
async def get_outer_ear_space_domain_analysis(
    ec_length: float, 
    fi: float, 
    ff: float, 
    nf: int, 
    freqs_of_analysis: List[float] = Query(...), 
    me_condition: Optional[str] = "healthy", 
    me_severity: Optional[str] = "low"
):

    if me_condition is None:
        me_condition = "healthy"
    if me_severity is None:
        me_severity = "low"

    freq_vec = np.linspace(fi,ff,nf)

    me_param = get_middle_ear_parameters("LVATB1")

    middle_ear_model = get_middle_ear_model(me_param,freq_vec,me_condition,me_severity)

    pressure, _, x_vec = eac_canal_acoustic_field(ec_length,me_param["tmArea"],freq_vec,middle_ear_model["Zme"])

    ind_freq = [np.argmin(abs(freq_vec - f)) for f in freqs_of_analysis]

    output = {
        "x_vec": x_vec.tolist()
    }

    for ind in ind_freq:
        output.update({f"{freqs_of_analysis[ind]}": np.real(pressure[ind, :]).tolist()})
    
    return output
