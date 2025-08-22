from __future__ import annotations
import numpy as np
import pandas as pd
import pytest

@pytest.fixture
def toy_prices() -> pd.DataFrame:
    n = 1000
    t = pd.date_range("2024-01-01", periods=n, freq="s").astype(str)
    rng = np.random.default_rng(0)
    latent = np.cumsum(0.001 * rng.standard_normal(n))
    noise = 0.005 * np.random.default_rng(1).standard_normal(n)
    price = 100 + latent + noise
    return pd.DataFrame({"timestamp": t, "price": price})
