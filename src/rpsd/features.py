from __future__ import annotations

import numpy as np


def sliding_windows(n: int, window: int, overlap: float) -> list[tuple[int, int]]:
    if not (0.0 <= overlap < 1.0):
        raise ValueError("overlap must be in [0,1)")
    if n <= 0:
        return [(0, 0)]
    if window <= 0 or window >= n:
        return [(0, n)]
    step = max(1, int(round(window * (1 - overlap))))
    bounds: list[tuple[int, int]] = []
    i = 0
    while i < n:
        j = min(i + window, n)
        bounds.append((i, j))
        if j == n:
            break
        i += step
        if i >= n:
            # ensure coverage of the end
            if bounds[-1][1] != n:
                bounds.append((max(n - window, 0), n))
            break
    # deduplicate and sort
    bounds = sorted(set(bounds))
    return bounds

def truncated_logsig(increments: np.ndarray, depth: int) -> np.ndarray:
    inc = np.asarray(increments, dtype=float)
    feats = [inc.mean(), inc.std(), np.mean(np.abs(inc))]
    if depth >= 2:
        feats += [np.mean(inc**2), np.mean(np.abs(inc)**1.5)]
    if depth >= 3:
        feats += [np.mean(inc**3)]
    return np.asarray(feats, dtype=float)

def pvar_proxy(increments: np.ndarray, p: float = 2.0) -> float:
    inc = np.asarray(increments, dtype=float)
    return float(np.sum(np.abs(inc) ** p))
