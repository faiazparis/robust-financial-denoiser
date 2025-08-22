from __future__ import annotations

import numpy as np
import pandas as pd


def to_series(time: pd.Series, values: np.ndarray, name: str) -> pd.Series:
    s = pd.Series(values, index=time, name=name)
    return s
