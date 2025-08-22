# Usage Guide

## Overview

The Robust Financial Time Series Denoiser provides a **fidelity-first approach** to financial signal processing, prioritizing signal preservation over aggressive noise removal.

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install -e .

# Install development dependencies (optional)
pip install -e .[dev]
```

### 2. Download Sample Data

```bash
python examples/download_data.py
```

This downloads Google (GOOG) 1-minute stock data for the last 5 trading days.

### 3. Run the Robust Denoiser

```bash
python examples/plot_real_data_robust.py
```

This generates:
- `examples/plots/goog_before_after_robust.png` - Google stock denoising plot
- Performance metrics in the terminal

## Core Components

### Robust Denoiser (`denoise_robust.py`)

The main denoising engine with comprehensive guardrails:

```python
from rpsd.denoise_robust import DenoiseConfig, wavelet_denoise, evaluate_guardrails

# Configure denoiser
config = DenoiseConfig(
    wavelet='db4',
    max_level_reduction=2,
    alpha=1.0,
    vol_adaptive=True,
    fir_apply=True,
    fir_cutoff_hz=1/600.0
)

# Apply denoising
denoised = wavelet_denoise(prices, config)

# Evaluate results
report = evaluate_guardrails(prices, denoised, config)
print(f"Compliance Score: {report.compliance_score:.1f}/100")
```

## Configuration

### DenoiseConfig Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `wavelet` | Wavelet family | 'db4' | 'haar', 'db1-20', 'sym2-20' |
| `max_level_reduction` | Level reduction from max | 2 | 0-5 |
| `alpha` | Threshold scaling factor | 1.0 | 0.1-3.0 |
| `vol_adaptive` | Volatility-adaptive thresholding | True | True/False |
| `fir_apply` | Apply FIR low-pass filter | True | True/False |
| `fir_cutoff_hz` | FIR cutoff frequency (Hz) | 1/600.0 | 1/3600.0-1/60.0 |

### Guardrail Thresholds

| Metric | Threshold | Description |
|--------|-----------|-------------|
| **Correlation** | ≥85% | Signal preservation |
| **RMSE** | ≤0.5 | Tracking accuracy |
| **Trend Agreement** | ≥90% | Slope preservation |
| **Low-freq Power** | ≥95% | Structure retention |
| **Residual Whiteness** | ≥0.05 | Statistical validity (p-value) |

## Data Format

### Required CSV Structure

```csv
timestamp,price
2025-08-18T13:30:00Z,205.08
2025-08-18T13:31:00Z,204.95
2025-08-18T13:32:00Z,205.16
...
```

**Columns:**
- `timestamp`: ISO8601 string or epoch timestamp
- `price`: Non-negative float (USD, EUR, etc.)

**Optional columns are ignored.**

### Data Quality Requirements

- **Minimum length**: 100 observations
- **Price range**: Positive values only
- **Time regularity**: Consistent intervals preferred
- **Missing data**: Handled automatically with interpolation

## Performance Metrics

### Primary Metrics

1. **Signal Correlation**: Signal preservation quality
2. **Signal Correlation**: Preservation of original structure
3. **RMSE**: Tracking accuracy
4. **Compliance Score**: Overall quality assessment (0-100)

### Secondary Metrics

1. **Trend Preservation**: Slope agreement percentage
2. **Low-frequency Power**: Structure retention
3. **Residual Whiteness**: Statistical validation
4. **Volatility Adaptation**: Market regime awareness

## Advanced Usage

### Custom Wavelet Selection

```python
import pywt

# List available wavelets
print(pywt.wavelist())

# Custom configuration
config = DenoiseConfig(
    wavelet='sym8',           # Symmetric wavelet
    max_level_reduction=1,    # Use more levels
    alpha=1.5,               # Higher threshold scaling
    vol_adaptive=False       # Disable volatility adaptation
)
```

### Parameter Optimization

```python
from rpsd.denoise_robust import search_params

# Find optimal parameters
best_config = search_params(
    prices,
    param_grid={
        'wavelet': ['db4', 'db8', 'sym8'],
        'max_level_reduction': [1, 2, 3],
        'alpha': [0.8, 1.0, 1.2]
    }
)
```

### Rolling Validation

```python
from rpsd.denoise_robust import rolling_validate

# Validate across time windows
results = rolling_validate(
    prices,
    window_size=1000,
    step_size=500,
    config=config
)
```

## Troubleshooting

### Common Issues

1. **Low correlation scores**: Reduce denoising intensity
2. **High RMSE**: Check data quality and preprocessing
3. **Compliance failures**: Adjust guardrail thresholds
4. **Memory errors**: Reduce window size or use chunking

### Performance Tuning

1. **Start conservative**: Use default parameters
2. **Monitor guardrails**: Watch compliance scores
3. **Adjust gradually**: Small parameter changes
4. **Validate results**: Always check final output

## Examples

### Basic Denoising

```python
import pandas as pd
from rpsd.denoise_robust import DenoiseConfig, wavelet_denoise

# Load data
df = pd.read_csv('data.csv')
prices = df['price'].values

# Configure and run
config = DenoiseConfig()
denoised = wavelet_denoise(prices, config)

# Save results
df['denoised'] = denoised
df.to_csv('denoised_data.csv', index=False)
```

### Batch Processing

```python
import glob
from pathlib import Path

# Process multiple files
for file_path in glob.glob('data/*.csv'):
    df = pd.read_csv(file_path)
    prices = df['price'].values
    
    denoised = wavelet_denoise(prices, config)
    
    output_path = Path(file_path).parent / f"denoised_{Path(file_path).name}"
    df['denoised'] = denoised
    df.to_csv(output_path, index=False)
```

## Best Practices

1. **Always validate**: Check guardrail compliance
2. **Start simple**: Use default configurations first
3. **Monitor performance**: Track metrics over time
4. **Document changes**: Keep parameter logs
5. **Test thoroughly**: Validate on multiple datasets

## Support

For issues and questions:
- Check the troubleshooting section above
- Review example scripts in `examples/`
- Open an issue on GitHub
- Check `docs/BACKGROUND.md` for theoretical context

## Project Structure

```
Rough Path Signal Denoiser/
├── src/rpsd/                    # Core implementation
│   ├── denoise_robust.py       # Robust wavelet denoiser
│   └── data.py                  # Data utilities
├── examples/                    # Usage examples
│   ├── download_data.py        # Data download utility
│   ├── plot_real_data_robust.py # Main plotting script
│   └── plots/                  # Generated visualizations
├── docs/                       # Documentation
├── tests/                      # Test suite
└── requirements.txt            # Dependencies
```
