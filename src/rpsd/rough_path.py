from __future__ import annotations

import numpy as np

from .features import pvar_proxy, truncated_logsig


def rough_metrics(increments: np.ndarray, sig_depth: int) -> dict[str, float]:
    logsig = truncated_logsig(increments, depth=sig_depth)
    return {
        "pvar2": pvar_proxy(increments, p=2.0),
        "logsig_l2": float(np.sum(logsig**2)),
        "mean_abs": float(np.mean(np.abs(increments))),
    }
