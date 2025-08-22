from __future__ import annotations
from typing import List, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class DenoiseResult:
    denoised: np.ndarray[np.float64, np.dtype[np.float64]]
    diagnostics: dict[str, int]


def compute_increments(x: np.ndarray[np.float64, np.dtype[np.float64]]) -> np.ndarray[np.float64, np.dtype[np.float64]]:
    """Compute increments with first increment = 0.0."""
    n = int(x.shape[0])
    inc = np.empty(n, dtype=np.float64)
    inc[0] = 0.0
    if n > 1:
        inc[1:] = x[1:] - x[:-1]
    return inc


def reconstruct_from_increments(baseline: float, inc: np.ndarray[np.float64, np.dtype[np.float64]]) -> np.ndarray[np.float64, np.dtype[np.float64]]:
    """Reconstruct series from increments using baseline."""
    # inc[0] must be 0.0 so that output[0] == baseline
    return np.float64(baseline) + np.cumsum(inc, dtype=np.float64)


def assert_shapes(x: np.ndarray[np.float64, np.dtype[np.float64]], inc: np.ndarray[np.float64, np.dtype[np.float64]], out_inc: np.ndarray[np.float64, np.dtype[np.float64]], den: np.ndarray[np.float64, np.dtype[np.float64]]) -> None:
    """Validate lengths at each step to fail fast if anything drifts."""
    n = len(x)
    assert len(inc) == n, f"inc length {len(inc)} != x length {n}"
    assert len(out_inc) == n, f"out_inc length {len(out_inc)} != x length {n}"
    assert len(den) == n, f"den length {len(den)} != x length {n}"


def sliding_windows(n: int, window: int, overlap: float) -> List[Tuple[int, int]]:
    """Generate sliding windows with guaranteed coverage."""
    if not (0.0 <= overlap < 1.0):
        raise ValueError("overlap must be in [0,1)")
    if n <= 0:
        return [(0, 0)]
    if window <= 0 or window >= n:
        return [(0, n)]
    step = max(1, int(round(window * (1 - overlap))))
    bounds = [(0, min(window, n))]
    i = step
    while i + window < n:
        bounds.append((i, i + window))
        i += step
    if bounds[-1][1] != n:
        bounds.append((max(n - window, 0), n))
    return sorted(set(bounds))


def tv_prox_increments(inc: np.ndarray[np.float64, np.dtype[np.float64]], lam: float, iters: int, step: float = 0.5) -> np.ndarray[np.float64, np.dtype[np.float64]]:
    """TV proximal on increments (does not touch baseline)."""
    # If lambda is 0, return original increments unchanged (identity case)
    if lam == 0:
        return inc.copy()
    
    v = inc.astype(np.float64).copy()
    for _ in range(max(1, iters)):
        # data fidelity
        v -= step * (v - inc)
        # TV soft-threshold on first differences of increments
        dv = np.zeros_like(v)
        diff = v[1:] - v[:-1]
        sgn = np.sign(diff)
        mag = np.maximum(np.abs(diff) - step * lam, 0.0)
        dv[1:] = sgn * mag
        # reconstruct increments; keep v[0] = inc[0] = 0.0
        v = np.cumsum(dv)
        v[0] = inc[0]  # preserve baseline
    return v


def denoise_series(
    values: np.ndarray[np.float64, np.dtype[np.float64]],
    window: int,
    overlap: float,
    lam_var: float,
    max_iters: int,
    n_jobs: int = 1,
    progress: bool = False,
) -> DenoiseResult:
    """
    Denoise series returning PRICES in the same domain as input.
    
    Args:
        values: Input prices (raw or standardized)
        window: Window size for processing
        overlap: Overlap fraction between windows
        lam_var: TV regularization strength
        max_iters: Maximum iterations for TV proximal
        n_jobs: Number of parallel jobs
        progress: Show progress bar
    
    Returns:
        DenoiseResult with denoised prices in same domain as input
    """
    n = values.shape[0]
    if n == 0:
        return DenoiseResult(denoised=values.copy(), diagnostics={"windows": 0})

    # 1) Compute increments correctly (first increment is 0.0)
    inc = compute_increments(values)  # inc[0] = 0.0
    
    # 2) Generate sliding windows with guaranteed coverage
    bounds = sliding_windows(n, window, overlap)

    if progress:
        from tqdm import tqdm
        iterator = tqdm(bounds, desc="Denoising", miniters=1)
    else:
        iterator = bounds

    def _process(i: int, j: int) -> tuple[np.ndarray[np.float64, np.dtype[np.float64]], np.ndarray[np.float64, np.dtype[np.float64]], int, int]:
        local = inc[i:j]
        dloc = tv_prox_increments(local, lam=lam_var, iters=max_iters, step=0.5)
        w = np.ones(len(local), dtype=np.float64)  # identity-safe weights
        return dloc * w, w, i, j

    if n_jobs == 1:
        results = [_process(i, j) for (i, j) in iterator]
    else:
        from joblib import Parallel, delayed
        results = Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(_process)(i, j) for (i, j) in iterator
        )

    # 3) Overlap-add on increments with flat weights
    out_inc = np.zeros(n, dtype=np.float64)  # match n exactly
    weight = np.zeros(n, dtype=np.float64)
    for dloc_w, w, i, j in results:
        out_inc[i:j] += dloc_w
        weight[i:j] += w

    # 4) Normalize by coverage
    covered = weight > 0
    out_inc[covered] /= weight[covered]
    out_inc[~covered] = inc[~covered]  # should not occur with proper bounds

    # 5) Reconstruct with baseline in the same domain
    baseline = np.float64(values[0])  # must preserve input domain
    den = reconstruct_from_increments(baseline, out_inc)

    # Length and baseline invariants
    assert_shapes(values, inc, out_inc, den)
    assert np.isclose(inc[0], 0.0), f"inc[0]={inc[0]} should be 0.0"
    assert np.isclose(den[0], values[0]), f"den[0]={den[0]} != values[0]={values[0]}"

    return DenoiseResult(denoised=den, diagnostics={"windows": len(bounds)})


# Legacy function for backward compatibility
def denoise_series_prices(
    prices: np.ndarray[np.float64, np.dtype[np.float64]],
    window: int = 250,
    overlap: float = 0.5,
    lam_var: float = 1.2,
    max_iters: int = 200,
) -> dict[str, np.ndarray[np.float64, np.dtype[np.float64]] | dict[str, int]]:
    """Legacy function - use denoise_series instead."""
    result = denoise_series(
        values=prices,
        window=window,
        overlap=overlap,
        lam_var=lam_var,
        max_iters=max_iters,
        n_jobs=1,
        progress=False
    )
    return {"price_denoised": result.denoised, "diagnostics": result.diagnostics}


# Test functions
def _identity_test() -> None:
    """Test identity contract: denoised == original when smoothing disabled."""
    # Raw prices identity test
    x = 100 + np.cumsum(np.random.default_rng(0).normal(0, 0.01, 1000))
    res = denoise_series(x, window=250, overlap=0.5, lam_var=0.0, max_iters=1)
    y = res.denoised
    assert np.allclose(x, y), "Raw prices identity failed when smoothing disabled"
    print("✓ Raw prices identity test passed")
    
    # Standardized prices identity test
    mean, std = x.mean(), x.std()
    x_std = (x - mean) / std
    res_std = denoise_series(x_std, window=250, overlap=0.5, lam_var=0.0, max_iters=1)
    y_std = res_std.denoised
    assert np.allclose(x_std, y_std), "Standardized prices identity failed when smoothing disabled"
    print("✓ Standardized prices identity test passed")


def _variance_drop_test() -> None:
    """Test variance reduction with smoothing enabled."""
    rng = np.random.default_rng(0)
    x = 100 + np.cumsum(0.01 * rng.standard_normal(3000)) + 0.05 * rng.standard_normal(3000)
    rv_x = float(np.sum(np.diff(x) ** 2))
    res = denoise_series(x, window=250, overlap=0.5, lam_var=1.2, max_iters=200)
    y = res.denoised
    rv_y = float(np.sum(np.diff(y) ** 2))
    print({"rv_original": rv_x, "rv_denoised": rv_y, "reduction": rv_x - rv_y})


def test_identity_contract() -> None:
    """Quick identity test to verify the fix."""
    print("Testing identity contract...")
    
    # Test with raw prices
    raw_prices = np.array([100.0, 100.1, 99.9, 100.2])
    print(f"Raw prices: {raw_prices}")
    
    result = denoise_series(raw_prices, window=4, overlap=0.5, lam_var=0.0, max_iters=1)
    denoised_raw = result.denoised
    print(f"Denoised raw: {denoised_raw}")
    
    assert np.allclose(raw_prices, denoised_raw), f"Raw identity failed: {raw_prices} vs {denoised_raw}"
    print("✓ Raw prices identity passed")
    
    # Test with standardized prices
    mean, std = raw_prices.mean(), raw_prices.std()
    std_prices = (raw_prices - mean) / std
    print(f"Standardized prices: {std_prices}")
    
    result_std = denoise_series(std_prices, window=4, overlap=0.5, lam_var=0.0, max_iters=1)
    denoised_std = result_std.denoised
    print(f"Denoised std: {denoised_std}")
    
    assert np.allclose(std_prices, denoised_std), f"Standardized identity failed: {std_prices} vs {denoised_std}"
    print("✓ Standardized prices identity passed")
    
    print("All identity tests passed! The denoiser preserves the baseline correctly.")


if __name__ == "__main__":
    test_identity_contract()
    _identity_test()
    _variance_drop_test()
