from __future__ import annotations
from rpsd.config import DenoiseConfig

def test_roundtrip(tmp_path):
    cfg = DenoiseConfig(window=128, max_iters=50, n_jobs=2)
    p = tmp_path / "cfg.json"
    cfg.save(p)
    loaded = DenoiseConfig.load(p)
    assert loaded.window == 128
    assert loaded.max_iters == 50
    assert loaded.n_jobs == 2
