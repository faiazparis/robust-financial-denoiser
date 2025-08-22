from __future__ import annotations

import numpy as np
import pandas as pd

from .features import pvar_proxy


def realized_variance(x: np.ndarray) -> float:
    dx = np.diff(x)
    return float(np.sum(dx * dx))

def eval_report(original: pd.Series, denoised: pd.Series) -> dict[str, float]:
    orig = original.to_numpy(dtype=float)
    den = denoised.to_numpy(dtype=float)
    rv_orig = realized_variance(orig)
    rv_den = realized_variance(den)
    pvar_orig = pvar_proxy(np.diff(orig))
    pvar_den = pvar_proxy(np.diff(den))
    return {
        "rv_original": rv_orig,
        "rv_denoised": rv_den,
        "rv_reduction": rv_orig - rv_den,
        "pvar_original": pvar_orig,
        "pvar_denoised": pvar_den,
        "pvar_reduction": pvar_orig - pvar_den,
    }
