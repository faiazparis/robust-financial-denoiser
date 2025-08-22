from __future__ import annotations
import pandas as pd
import pytest
from rpsd.data import read_ticks, preprocess_prices

def test_read_ticks_ok(tmp_path):
    p = tmp_path / "ok.csv"
    pd.DataFrame({"timestamp": ["2024-01-01T00:00:00","2024-01-01T00:00:01"], "price": [100.0, 100.1]}).to_csv(p, index=False)
    df = read_ticks(p, "timestamp", "price")
    assert len(df) == 2

def test_empty_csv(tmp_path):
    p = tmp_path / "empty.csv"
    pd.DataFrame(columns=["timestamp","price"]).to_csv(p, index=False)
    with pytest.raises(ValueError):
        read_ticks(p, "timestamp", "price")

def test_negative_prices(tmp_path):
    p = tmp_path / "neg.csv"
    pd.DataFrame({"timestamp": ["2024-01-01T00:00:00","2024-01-01T00:00:01"], "price": [100.0, -1.0]}).to_csv(p, index=False)
    with pytest.raises(ValueError):
        read_ticks(p, "timestamp", "price")

def test_irregular_timestamps(tmp_path):
    p = tmp_path / "irreg.csv"
    pd.DataFrame({"timestamp": ["2024-01-01T00:00:00","foo","2024-01-01T00:00:03"], "price": [100.0, 101.0, 102.0]}).to_csv(p, index=False)
    out = read_ticks(p, "timestamp", "price")
    assert len(out) == 2

def test_preprocess_standardize(toy_prices: pd.DataFrame):
    df, mean, std = preprocess_prices(toy_prices, "price", clip_z=8.0, standardize=True)
    assert abs(df["price"].mean()) < 1e-6
    assert std > 0.0
