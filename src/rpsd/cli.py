from __future__ import annotations

from pathlib import Path

import pandas as pd
import typer
from rich.console import Console
import numpy as np

from .config import DenoiseConfig
from .data import preprocess_prices, read_ticks
from .denoise import denoise_series
from .evaluation import eval_report

app = typer.Typer(help="Robust Financial Time Series Denoiser (RPSD)")
console = Console()

@app.command()
def denoise(
    input: str = typer.Option(..., help="Input CSV path"),
    output: str = typer.Option(..., help="Output CSV path"),
    time_col: str = typer.Option("timestamp"),
    price_col: str = typer.Option("price"),
    window: int = typer.Option(150),
    overlap: float = typer.Option(0.5),
    lambda_var: float = typer.Option(0.5),
    max_iters: int = typer.Option(80),
    n_jobs: int = typer.Option(1, help="-1 to use all cores"),
    progress: bool = typer.Option(False),
    verbose: bool = typer.Option(False),
    clip_z: float = typer.Option(8.0, help="Robust outlier clipping on increments (z-threshold)"),
    standardize: bool = typer.Option(True, help="Standardize before denoising and undo afterward"),
) -> None:
    cfg = DenoiseConfig(
        time_col=time_col, price_col=price_col, window=window, overlap=overlap,
        lambda_var=lambda_var, max_iters=max_iters, n_jobs=n_jobs, verbose=verbose,
        clip_z=clip_z, standardize=standardize
    )
    if verbose:
        console.log(f"Loading CSV: {input}")
    df = read_ticks(input, time_col, price_col)
    
    # Single standardization point: preprocess once
    df_p, mean, std = preprocess_prices(df, price_col, clip_z, standardize)
    values = df_p[price_col].to_numpy(dtype=float)
    
    if verbose:
        console.log(f"Preprocessing: standardize={standardize}, mean={mean:.6f}, std={std:.6f}")
        console.log(f"First few input values: {values[:3]}")

    # Denoise in the same domain as input (standardized or raw)
    res = denoise_series(
        values=values,
        window=cfg.window,
        overlap=cfg.overlap,
        lam_var=cfg.lambda_var,
        max_iters=cfg.max_iters,
        n_jobs=cfg.n_jobs,
        progress=progress
    )

    # Inverse transform exactly once on FINAL PRICES (not on increments)
    if standardize:
        out_values = res.denoised * std + mean
        if verbose:
            console.log(f"First few denoised standardized: {res.denoised[:3]}")
            console.log(f"First few after inverse transform: {out_values[:3]}")
    else:
        out_values = res.denoised
        if verbose:
            console.log(f"First few denoised raw: {out_values[:3]}")
    
    # Sanity checks for identity contract
    if verbose:
        if standardize:
            # Check that inverse scaling preserves the relationship
            assert np.isclose(out_values[0], df[price_col].iloc[0], rtol=1e-10), \
                f"Inverse scaling baseline mismatch: {out_values[0]} != {df[price_col].iloc[0]}"
        else:
            # Check that raw processing preserves baseline
            assert np.isclose(out_values[0], df[price_col].iloc[0], rtol=1e-10), \
                f"Raw processing baseline mismatch: {out_values[0]} != {df[price_col].iloc[0]}"
    
    out = pd.DataFrame({time_col: df[time_col].astype(str), price_col: out_values})
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    cfg.save(Path(output).with_suffix(".config.json"))
    if verbose:
        console.log(f"Diagnostics: {res.diagnostics}")
    console.print(f"[bold green]Saved denoised CSV:[/bold green] {output}")

@app.command()
def evaluate(
    original: str = typer.Option(...),
    denoised: str = typer.Option(...),
    time_col: str = typer.Option("timestamp"),
    price_col: str = typer.Option("price"),
) -> None:
    df_o = pd.read_csv(original)
    df_d = pd.read_csv(denoised)
    need = {time_col, price_col}
    if not need.issubset(df_o.columns) or not need.issubset(df_d.columns):
        raise ValueError("Both CSVs must contain time and price columns")
    m = df_o[[time_col, price_col]].merge(df_d[[time_col, price_col]], on=time_col, suffixes=("_orig", "_den"))
    report = eval_report(m[f"{price_col}_orig"], m[f"{price_col}_den"])
    for k, v in report.items():
        console.print(f"{k}: {v:.6f}")

if __name__ == "__main__":
    app()
