# Install (Local-First)

## Basic Installation

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
pre-commit install
```

## Quality Checks

```bash
pre-commit run --all-files
pytest -q
mypy src
ruff check src
```

## Verification

After installation, verify the system works correctly:

```bash
# Test identity contract (should return exact input)
python -c "
from src.rpsd.denoise import test_identity_contract
test_identity_contract()
"

# Test CLI functionality
rpsd --help

# Test on sample data
python examples/download_data.py
rpsd denoise --input examples/goog_1m.csv --output examples/goog_identity.csv \
  --window 150 --overlap 0.5 --lambda-var 0.0 --max-iters 1 --verbose
```

## Expected Results

- ✅ **Identity Test**: All tests should pass with "✓ Identity test passed"
- ✅ **CLI Help**: Should display help information
- ✅ **Identity Contract**: Output should equal input exactly when `lambda-var=0.0`
- ✅ **No Errors**: All operations should complete without errors or warnings

## Troubleshooting

If you encounter issues:

1. **Check Python version**: Ensure you're using Python 3.11+
2. **Verify virtual environment**: Make sure `.venv` is activated
3. **Check dependencies**: Run `pip list` to verify all packages installed
4. **Run tests**: Execute `pytest -q` to identify any test failures
5. **Check logs**: Use `--verbose` flag to see detailed operation logs
