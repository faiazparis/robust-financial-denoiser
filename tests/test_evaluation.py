from __future__ import annotations
import numpy as np
import pandas as pd
from rpsd.evaluation import eval_report

def test_eval_report_keys():
    n = 100
    t = pd.date_range("2024-01-01", periods=n, freq="s").astype(str)
    x = 100 + np.cumsum(np.random.default_rng(0).normal(0, 1.0, n))
    y = x + 0.1*np.random.default_rng(1).normal(0, 1.0, n)
    df = pd.DataFrame({"timestamp": t, "x": x, "y": y})
    rep = eval_report(df["x"], df["y"])
    assert "rv_original" in rep and "pvar_denoised" in rep
