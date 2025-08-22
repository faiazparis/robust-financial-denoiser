import pandas as pd
import numpy as np
from pathlib import Path

n = 10_000
t = pd.date_range("2024-01-01", periods=n, freq="s")
rng = np.random.default_rng(0)
latent = np.cumsum(0.003 * rng.standard_normal(n))
micro = 0.01 * rng.standard_normal(n)
price = 100 + latent + micro
Path("examples").mkdir(parents=True, exist_ok=True)
pd.DataFrame({"timestamp": t.astype(str), "price": price}).to_csv("examples/sample_ticks_10k.csv", index=False)
print("Wrote examples/sample_ticks_10k.csv")
