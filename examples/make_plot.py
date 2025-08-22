import pandas as pd
import matplotlib.pyplot as plt
import subprocess, sys
from pathlib import Path

raw = "examples/sample_ticks_10k.csv"
den = "examples/denoised.csv"

# Ensure sample exists
if not Path(raw).exists():
    import examples.generate_sample_10k  # noqa: F401

# Run denoise via CLI
subprocess.run([sys.executable, "-m", "rpsd.cli", "denoise", "--input", raw, "--output", den, "--progress"], check=True)

df_o = pd.read_csv(raw)
df_d = pd.read_csv(den)
m = df_o.merge(df_d, on="timestamp", suffixes=("_orig","_den"))

plt.figure(figsize=(10,4))
N = min(2000, len(m))
plt.plot(m["timestamp"][:N], m["price_orig"][:N], alpha=0.5, label="original")
plt.plot(m["timestamp"][:N], m["price_den"][:N], alpha=0.9, label="denoised")
plt.legend()
plt.xticks([])
plt.tight_layout()
Path("examples/plots").mkdir(parents=True, exist_ok=True)
plt.savefig("examples/plots/before_after.png", dpi=160)
print("Wrote examples/plots/before_after.png")
