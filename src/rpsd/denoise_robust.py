# denoise_robust.py
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple, List
import pywt
from scipy.signal import firwin, filtfilt
from statsmodels.stats.diagnostic import acorr_ljungbox

# --------------------------
# Utilities
# --------------------------

def realized_vol(x: np.ndarray, window: int = 60) -> np.ndarray:
    dx = np.diff(x, prepend=x[0])
    rv = pd.Series(dx**2).rolling(window, min_periods=1).sum().values
    return np.sqrt(np.maximum(rv, 1e-12))

def rolling_slope(x: np.ndarray, window: int = 30) -> np.ndarray:
    # Fast rolling slope via cumulative sums (least squares over window)
    n = len(x)
    w = window
    if n < w:
        w = n
    idx = np.arange(n)
    c1 = pd.Series(idx).rolling(w, min_periods=1).sum().values
    c2 = pd.Series(idx**2).rolling(w, min_periods=1).sum().values
    y1 = pd.Series(x).rolling(w, min_periods=1).sum().values
    y2 = pd.Series(x*idx).rolling(w, min_periods=1).sum().values
    denom = (w * c2 - c1**2)
    denom = np.where(np.abs(denom) < 1e-12, 1e-12, denom)
    slope = (w * y2 - c1 * y1) / denom
    return slope

def sign_agreement(a: np.ndarray, b: np.ndarray) -> float:
    sa = np.sign(a)
    sb = np.sign(b)
    mask = (sa != 0) | (sb != 0)
    if mask.sum() == 0:
        return 1.0
    return (sa[mask] == sb[mask]).mean()

def bayes_shrink_threshold(detail_coeffs: np.ndarray) -> float:
    # BayesShrink style threshold
    var = np.var(detail_coeffs)
    if var <= 0:
        return 0.0
    sigma = np.median(np.abs(detail_coeffs)) / 0.6745 + 1e-12
    var_sig = max(var - sigma**2, 0.0)
    if var_sig <= 0:
        return np.max(np.abs(detail_coeffs))  # shrink all if pure noise
    return (sigma**2) / np.sqrt(var_sig + 1e-12)

def soft_threshold(x: np.ndarray, thr: float) -> np.ndarray:
    return np.sign(x) * np.maximum(np.abs(x) - thr, 0.0)

def zero_phase_lowpass(x: np.ndarray, cutoff_hz: float, fs_hz: float, numtaps: int = 101) -> np.ndarray:
    cutoff_norm = cutoff_hz / (fs_hz / 2.0)
    cutoff_norm = min(max(cutoff_norm, 1e-6), 0.999999)
    taps = firwin(numtaps, cutoff_norm, window='hann')
    return filtfilt(taps, [1.0], x, padlen=min(3*max(len(taps), 1), max(5, len(x)//2)))

def psd_band_power(x: np.ndarray, fs_hz: float, split_hz: float) -> Tuple[float, float]:
    # Simple Welch-free PSD estimate via FFT
    n = int(2 ** np.floor(np.log2(len(x))))
    if n < 8:
        return 0.0, 0.0
    xz = x - np.mean(x)
    X = np.fft.rfft(xz[:n])
    freqs = np.fft.rfftfreq(n, d=1/fs_hz)
    power = (np.abs(X)**2) / n
    low_mask = freqs <= split_hz
    return power[low_mask].sum(), power[~low_mask].sum()

# --------------------------
# Config
# --------------------------

@dataclass
class DenoiseConfig:
    wavelet: str = "db4"
    max_level_reduction: int = 2  # lower removes fewer low-freq levels
    alpha: float = 1.0            # scales BayesShrink threshold
    vol_adaptive: bool = True
    vol_window: int = 60
    fir_apply: bool = False
    fir_cutoff_hz: float = 0.01   # relative to fs_hz
    fir_taps: int = 101
    fs_hz: float = 1.0            # samples per second (e.g., minute bars ~ 1/60 Hz)
    # Guardrails
    min_correlation: float = 0.85
    min_trend_agreement: float = 0.9
    min_lowfreq_power_preserve: float = 0.95
    lowfreq_split_hz: float = 0.003

# --------------------------
# Core: Wavelet denoiser
# --------------------------

def wavelet_denoise(x: np.ndarray, cfg: DenoiseConfig) -> np.ndarray:
    # Decompose
    max_level = pywt.dwt_max_level(len(x), pywt.Wavelet(cfg.wavelet).dec_len)
    # Keep approximation up to (max_level - max_level_reduction)
    level = max(1, max_level - cfg.max_level_reduction)

    coeffs = pywt.wavedec(x, cfg.wavelet, mode="periodization", level=level)
    cA = coeffs[0]
    details = coeffs[1:]

    # Volatility-adaptive scaling
    if cfg.vol_adaptive:
        vol = realized_vol(x, cfg.vol_window)
        scale = np.clip(vol / (np.median(vol) + 1e-12), 0.5, 2.0)
        # Map to a single scalar per level: use median of recent scale
        alpha_scale = np.median(scale)
    else:
        alpha_scale = 1.0

    # Threshold detail coefficients (high frequency)
    new_details = []
    for d in details:
        thr = bayes_shrink_threshold(d) * cfg.alpha * alpha_scale
        new_details.append(soft_threshold(d, thr))

    y = pywt.waverec([cA] + new_details, cfg.wavelet, mode="periodization")

    # Optional zero-phase low-pass for mild residual smoothing
    if cfg.fir_apply:
        y = zero_phase_lowpass(y, cfg.fir_cutoff_hz * cfg.fs_hz, cfg.fs_hz, cfg.fir_taps)

    # Match length
    y = y[:len(x)]
    return y

# --------------------------
# Guardrail evaluation
# --------------------------

@dataclass
class DenoiseReport:
    corr: float
    rmse: float
    trend_agreement: float
    lowfreq_preserve: float
    residual_white_pval: float
    passes: bool
    meta: Dict[str, Any]

def evaluate_guardrails(x: np.ndarray, y: np.ndarray, cfg: DenoiseConfig) -> DenoiseReport:
    x = np.asarray(x)
    y = np.asarray(y)

    # Correlation and RMSE
    if np.std(x) < 1e-12 or np.std(y) < 1e-12:
        corr = 0.0
    else:
        corr = float(np.corrcoef(x, y)[0,1])
    rmse = float(np.sqrt(np.mean((x - y)**2)))

    # Trend agreement via rolling slope sign
    slope_x = rolling_slope(x, window=30)
    slope_y = rolling_slope(y, window=30)
    trend_agree = float(sign_agreement(slope_x, slope_y))

    # Low-frequency power preservation
    low_x, high_x = psd_band_power(x, cfg.fs_hz, cfg.lowfreq_split_hz)
    low_y, high_y = psd_band_power(y, cfg.fs_hz, cfg.lowfreq_split_hz)
    low_preserve = 0.0 if low_x <= 0 else float(min(low_y / low_x, 1.0))

    # Residual whiteness
    resid = x - y
    try:
        lb = acorr_ljungbox(resid, lags=[20], return_df=True)
        pval = float(lb["lb_pvalue"].iloc)
    except Exception:
        pval = 0.0

    passes = (
        corr >= cfg.min_correlation and
        trend_agree >= cfg.min_trend_agreement and
        low_preserve >= cfg.min_lowfreq_power_preserve and
        pval >= 0.05  # residual close to white noise
    )

    return DenoiseReport(
        corr=corr,
        rmse=rmse,
        trend_agreement=trend_agree,
        lowfreq_preserve=low_preserve,
        residual_white_pval=pval,
        passes=passes,
        meta={}
    )

# --------------------------
# Parameter search (small)
# --------------------------

def search_params(x: np.ndarray, cfg: DenoiseConfig,
                  alpha_grid=(0.5, 1.0, 1.5),
                  level_reduction_grid=(1, 2, 3),
                  fir_apply_grid=(False, True)) -> Tuple[np.ndarray, DenoiseReport, DenoiseConfig]:
    best_score = -np.inf
    best = (None, None, None)
    for a in alpha_grid:
        for lr in level_reduction_grid:
            for fa in fir_apply_grid:
                trial = DenoiseConfig(**{**cfg.__dict__, "alpha": a, "max_level_reduction": lr, "fir_apply": fa})
                y = wavelet_denoise(x, trial)
                rep = evaluate_guardrails(x, y, trial)
                # Score: prioritize correlation and trend agreement; penalize RMSE
                score = 2.0*rep.corr + 1.0*rep.trend_agreement - 0.25*rep.rmse
                # Enforce hard fails to rank lower
                if not rep.passes:
                    score -= 10.0
                if score > best_score:
                    best_score = score
                    best = (y, rep, trial)
    return best
