from __future__ import annotations
import numpy as np
from rpsd.denoise import denoise_series

def test_denoise_series_shapes():
    n = 500
    x = 100 + np.cumsum(np.random.default_rng(0).normal(0, 0.01, n))
    res = denoise_series(x, window=100, overlap=0.5, lam_var=1.0, lam_sig=0.1, sig_depth=2, max_iters=50, n_jobs=1)
    assert res.denoised.shape == x.shape

def test_variance_non_increase():
    n = 2000
    rng = np.random.default_rng(0)
    x = 100 + np.cumsum(0.01 * rng.standard_normal(n)) + 0.05 * rng.standard_normal(n)
    res = denoise_series(x, window=200, overlap=0.5, lam_var=1.0, lam_sig=0.1, sig_depth=2, max_iters=50)
    assert np.var(np.diff(res.denoised)) <= np.var(np.diff(x)) + 1e-9

def test_tiny_input():
    x = np.array([100.0, 100.1, 99.9, 100.0])
    res = denoise_series(x, window=8, overlap=0.5, lam_var=0.5, lam_sig=0.1, sig_depth=2, max_iters=10)
    assert res.denoised.shape == x.shape
