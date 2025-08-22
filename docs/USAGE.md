# Usage

Denoise:
```bash
rpsd denoise --input data.csv --output out.csv --time-col timestamp --price-col price \
  --window 150 --overlap 0.5 --sig-depth 2 --lambda-var 0.5 --lambda-sig 0.1 \
  --max-iters 80 --n-jobs -1 --progress
```

Evaluate:
```bash
rpsd evaluate --original data.csv --denoised out.csv --time-col timestamp --price-col price
```
