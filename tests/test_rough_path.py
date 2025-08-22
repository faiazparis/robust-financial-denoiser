from __future__ import annotations
import numpy as np
from rpsd.rough_path import rough_metrics

def test_rough_metrics_keys():
    inc = np.array([0.1, -0.2, 0.05])
    m = rough_metrics(inc, 2)
    assert "pvar2" in m and "logsig_l2" in m and "mean_abs" in m
