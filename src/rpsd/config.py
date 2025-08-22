from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DenoiseConfig:
    time_col: str = "timestamp"
    price_col: str = "price"
    window: int = 150
    overlap: float = 0.5
    lambda_var: float = 0.5
    max_iters: int = 80
    n_jobs: int = 1
    verbose: bool = False
    clip_z: float | None = 8.0
    standardize: bool = True
    seed: int = 42

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2))

    @staticmethod
    def load(path: str | Path) -> DenoiseConfig:
        obj = json.loads(Path(path).read_text())
        return DenoiseConfig(**obj)
