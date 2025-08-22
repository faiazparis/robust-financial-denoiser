from __future__ import annotations

from pathlib import Path

import pandas as pd
import typer
from rich.console import Console

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
    sig_depth: int = typer.Option(2),
    lambda_var: float = typer.Option(0.5),
    lambda_sig: float = typer.Option(0.1),
    max_iters: int = typer.Option(80),
    n_jobs: int = typer.Option(1, help="-1 to use all cores"),
    progress: bool = typer.Option(False),
    verbose: bool = typer.Option(False),
    clip_z: float = typer.Option(8.0, help="Robust outlier clipping on increments (z-threshold)"),
    standardize: bool = typer.Option(True, help="Standardize before denoising and undo afterward"),
) -> None:
    cfg = DenoiseConfig(
        time_col=time_col, price_col=price_col, window=window, overlap=overlap,
        sig_depth=sig_depth, lambda_var=lambda_var, lambda_sig=lambda_sig,
        max_iters=max_iters, n_jobs=n_jobs, verbose=verbose,
        clip_z=clip_z, standardize=standardize
    )
    if verbose:
        console.log(f"Loading CSV: {input}")
    df = read_ticks(input, time_col, price_col)
    df_p, mean, std = preprocess_prices(df, price_col, clip_z, standardize)
    values = df_p[price_col].to_numpy(dtype=float)

    res = denoise_series(
        values, window=cfg.window, overlap=cfg.overlap,
        lam_var=cfg.lambda_var, lam_sig=cfg.lambda_sig, sig_depth=cfg.sig_depth,
        max_iters=cfg.max_iters, n_jobs=cfg.n_jobs, progress=progress
    )

    out_values = res.denoised * (std if standardize else 1.0) + (mean if standardize else 0.0)
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
