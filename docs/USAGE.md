# Usage

## Basic Denoising

Denoise with smoothing:
```bash
rpsd denoise --input data.csv --output out.csv --time-col timestamp --price-col price \
  --window 250 --overlap 0.5 --lambda-var 1.2 --max-iters 200 --n-jobs -1 --progress
```

## Testing the Identity Contract

Test that the denoiser preserves input exactly when smoothing is disabled:
```bash
rpsd denoise --input data.csv --output identity_test.csv --window 150 --overlap 0.5 \
  --lambda-var 0.0 --max-iters 1 --verbose
```

This should return output identical to input, verifying the mathematical foundation.

## Parameter Guide

- **`--window`**: Window size for processing (default: 150, recommended: 250 for real data)
- **`--overlap`**: Overlap fraction between windows (default: 0.5)
- **`--lambda-var`**: TV regularization strength (0.0 = identity, 1.2 = medium smoothing, 3.0+ = heavy smoothing)
- **`--max-iters`**: Maximum iterations for TV proximal (default: 80, recommended: 200 for real data)
- **`--standardize`**: Standardize prices before processing (default: true)
- **`--n-jobs`**: Number of parallel jobs (-1 for all cores)

## Evaluation

Evaluate denoising results:
```bash
rpsd evaluate --original data.csv --denoised out.csv --time-col timestamp --price-col price
```

## Complete Example Workflow

```bash
# 1. Test identity contract (should return exact input)
rpsd denoise --input examples/goog_1m.csv --output examples/goog_identity.csv \
  --window 150 --overlap 0.5 --lambda-var 0.0 --max-iters 1 --verbose

# 2. Denoise with smoothing
rpsd denoise --input examples/goog_1m.csv --output examples/goog_denoised.csv \
  --window 250 --overlap 0.5 --lambda-var 1.2 --max-iters 200 --verbose

# 3. Evaluate results
rpsd evaluate --original examples/goog_1m.csv --denoised examples/goog_denoised.csv

# 4. Generate plots
python examples/plot_real_data.py
```

## Expected Results

- **Identity Test**: Output should equal input exactly when `lambda-var=0.0`
- **Smoothing**: Progressive noise reduction with increasing `lambda-var`
- **Baseline Preservation**: First price preserved exactly across all operations
- **Length Stability**: No array length mismatches or data loss
