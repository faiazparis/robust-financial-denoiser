from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _parse_time(col: pd.Series) -> pd.Series:
    try:
        t = pd.to_datetime(col, errors="coerce", utc=False)
    except Exception:
        t = pd.Series(pd.NaT, index=col.index)
    if t.isna().all():
        raise ValueError("All timestamps failed to parse; ensure ISO8601 or epoch integers")
    return t

def read_ticks(csv_path: str | Path, time_col: str, price_col: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("Empty CSV")
    if time_col not in df.columns or price_col not in df.columns:
        raise ValueError(f"Missing required columns: {time_col}, {price_col}")
    df = df[[time_col, price_col]].copy()
    df[time_col] = _parse_time(df[time_col])
    df = df.dropna(subset=[time_col, price_col])
    df[price_col] = df[price_col].astype(float)
    if (df[price_col] < 0).any():
        raise ValueError("Negative prices found")
    df = df.sort_values(time_col).reset_index(drop=True)
    return df

def robust_zscore(x: np.ndarray) -> np.ndarray:
    med = np.median(x)
    mad = np.median(np.abs(x - med)) + 1e-12
    return (x - med) / (1.4826 * mad)

def preprocess_prices(df: pd.DataFrame, price_col: str, clip_z: float | None, standardize: bool) -> tuple[pd.DataFrame, float, float]:
    """Preprocess prices with optional standardization."""
    x = df[price_col].to_numpy(dtype=float)
    
    # Skip outlier clipping for now to avoid length issues
    # TODO: Implement robust outlier clipping that preserves baseline and length
    
    mean, std = (0.0, 1.0)
    if standardize:
        mean = float(np.mean(x))
        std = float(np.std(x) + 1e-12)
        x = (x - mean) / std
    
    out = df.copy()
    out[price_col] = x
    return out, mean, std
