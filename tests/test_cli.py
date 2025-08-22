from __future__ import annotations
import pandas as pd
from typer.testing import CliRunner
from rpsd.cli import app

def test_cli_roundtrip(tmp_path):
    p_in = tmp_path / "ticks.csv"
    df = pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=100, freq="s").astype(str), "price": 100.0})
    df.to_csv(p_in, index=False)
    p_out = tmp_path / "den.csv"
    r = CliRunner().invoke(app, ["denoise", "--input", str(p_in), "--output", str(p_out), "--progress"])
    assert r.exit_code == 0
