from __future__ import annotations
import numpy as np
from rpsd.features import truncated_logsig, pvar_proxy

def test_truncated_logsig_shape():
    inc = np.array([0.0, 1.0, -1.0])
    f = truncated_logsig(inc, 2)
    assert f.ndim == 1
    assert len(f) >= 3

def test_pvar_proxy_value():
    inc = np.array([1.0, -2.0, 3.0])
    v = pvar_proxy(inc, 2.0)
    assert v == 14.0
