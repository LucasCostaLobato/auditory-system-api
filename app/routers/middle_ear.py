from fastapi import APIRouter, HTTPException, Query
import numpy as np
from typing import List, Optional

from app.models.middle_ear.deterministic_models import get_middle_ear_model

router = APIRouter(prefix="/middle-ear", tags=["middleear"])


@router.get("/frf")
async def get_middle_ear_frf(
    fi: float,
    ff: float,
    nf: int,
    me_condition: Optional[str] = "healthy",
    me_severity: Optional[str] = "low",
    measures: List[str] = Query(...),
):
    
    freq_vec, middle_ear_model = get_middle_ear_model(
        fi,
        ff,
        nf,
        me_condition,
        me_severity,
    )

    output = {"freq_vec": freq_vec.tolist()}

    for measure in measures:
        output.update(
            {f"{measure}": np.abs(middle_ear_model[measure]).tolist()}
        )

    return output