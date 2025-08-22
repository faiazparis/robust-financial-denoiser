# Install (Local-First)

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
pre-commit install
```

Checks:
```bash
pre-commit run --all-files
pytest -q
mypy src
ruff check src
```
