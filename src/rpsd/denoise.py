from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm

from .features import sliding_windows, truncated_logsig


@dataclass
class DenoiseResult:
    denoised: np.ndarray
    diagnostics: dict

def _proximal_tv(increments: np.ndarray, lam: float, iters: int, step: float) -> np.ndarray:
    v = increments.astype(float).copy()
    for _ in range(max(1, iters)):
        # gradient step for 0.5||v - increments||^2
        v -= step * (v - increments)
        # soft-threshold on first differences of v
        dv = np.empty_like(v)
        dv = v
        diff = v[1:] - v[:-1]
        sgn = np.sign(diff)
        mag = np.maximum(np.abs(diff) - step * lam, 0.0)
        dv[1:] = sgn * mag
        v = np.cumsum(dv)
    return v

def _fit_window(increments: np.ndarray, lam_var: float, lam_sig: float, sig_depth: int, iters: int) -> np.ndarray:
    v = _proximal_tv(increments, lam=lam_var, iters=iters, step=0.5)
    obs = truncated_logsig(increments, depth=sig_depth)
    den = truncated_logsig(v, depth=sig_depth)
    v = v + 0.1 * (np.mean(obs - den))
    return v

def _process_window(inc: np.ndarray, i: int, j: int, lam_var: float, lam_sig: float, sig_depth: int, iters: int) -> tuple[np.ndarray, np.ndarray, int, int]:
    local = inc[i:j]
    dloc = _fit_window(local, lam_var=lam_var, lam_sig=lam_sig, sig_depth=sig_depth, iters=iters)
    w = np.hanning(len(local)) if len(local) > 2 else np.ones(len(local))
    return dloc * w, w, i, j

def denoise_series(values: np.ndarray, window: int, overlap: float, lam_var: float, lam_sig: float, sig_depth: int, max_iters: int = 80, n_jobs: int = 1, progress: bool = False) -> DenoiseResult:
    n = len(values)
    if n == 0:
        return DenoiseResult(denoised=np.array([], dtype=float), diagnostics={"windows": 0})
    inc = np.diff(values, prepend=values[0])
    bounds = sliding_windows(n, window, overlap)

    iterator = bounds
    if progress:
        iterator = tqdm(bounds, desc="Denoising", miniters=1)

    results = Parallel(n_jobs=n_jobs, prefer="threads")(
        delayed(_process_window)(inc, i, j, lam_var, lam_sig, sig_depth, max_iters) for (i, j) in iterator
    )

    out_inc = np.zeros_like(inc, dtype=float)
    weight = np.zeros_like(inc, dtype=float)
    for dloc_w, w, i, j in results:
        out_inc[i:j] += dloc_w
        weight[i:j] += w
    weight = np.where(weight == 0.0, 1.0, weight)
    out_inc /= weight
    den = np.cumsum(out_inc)
    return DenoiseResult(denoised=den, diagnostics={"windows": len(bounds), "n_jobs": n_jobs})
