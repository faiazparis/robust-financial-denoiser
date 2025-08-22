# Installation Guide

## Overview

This guide covers installing and setting up the Robust Financial Time Series Denoiser. The system is designed to work with Python 3.11+ and provides a programmatic interface.

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.11 or higher (3.12 recommended)
- **Memory**: At least 4GB RAM for large datasets
- **Storage**: 1GB free space for installation and data

### Python Environment

We recommend using a virtual environment to avoid dependency conflicts:

```bash
# Check Python version
python3.11 --version

# Create virtual environment
python3.11 -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

## Installation Methods

### Method 1: Development Installation (Recommended)

For development and testing:

```bash
# Clone repository
git clone https://github.com/faiazparis/robust-financial-denoiser.git
cd robust-financial-denoiser

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]
```

### Method 2: PyPI Installation

For production use (when available):

```bash
pip install robust-financial-denoiser
```

### Method 3: Source Installation

For custom modifications:

```bash
# Download and extract source
wget https://github.com/faiazparis/robust-financial-denoiser/archive/main.zip
unzip main.zip
cd robust-financial-denoiser-main

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

## Dependencies

### Core Dependencies

The following packages are automatically installed:

- **NumPy**: Numerical computing foundation
- **Pandas**: Data manipulation and analysis
- **SciPy**: Scientific computing utilities
- **PyWavelets**: Wavelet analysis and denoising
- **scikit-learn**: Machine learning utilities
- **statsmodels**: Statistical modeling
- **Matplotlib**: Plotting and visualization
- **yfinance**: Financial data access

### Development Dependencies

Optional packages for development:

- **pytest**: Testing framework
- **mypy**: Type checking
- **ruff**: Code linting and formatting
- **black**: Code formatting
- **pre-commit**: Git hooks for code quality

## Configuration

### Environment Variables

Set these optional environment variables:

```bash
# Data directory
export RPSD_DATA_DIR=/path/to/data

# Logging level
export RPSD_LOG_LEVEL=INFO

# Cache directory
export RPSD_CACHE_DIR=/path/to/cache
```

### Configuration Files

Create a configuration file at `~/.rpsd/config.yaml`:

```yaml
# Default denoiser settings
denoiser:
  wavelet: db4
  level: 4
  threshold_mode: bayes
  use_fir_filter: true
  fir_cutoff: 0.1

# Guardrail thresholds
guardrails:
  correlation_threshold: 0.85
  rmse_threshold: 0.5
  trend_threshold: 0.90
  power_threshold: 0.95

# Data processing
data:
  standardize: true
  clip_outliers: false
  interpolate_missing: true
```

## Verification

### Basic Test

Verify the installation works:

```bash
# Test import
python -c "import rpsd; print('Import successful')"

# Run basic test
python -m pytest tests/test_basic.py -v
```

### Performance Test

Test with sample data:

```bash
# Download test data
python examples/download_data.py

# Run denoiser
python examples/plot_real_data_robust.py

# Check output
ls examples/plots/
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Reinstall package
   pip uninstall rpsd
   pip install -e .
   ```

2. **Missing Dependencies**
   ```bash
   # Update pip
   pip install --upgrade pip
   
   # Install missing packages
   pip install -r requirements.txt
   ```

3. **Version Conflicts**
   ```bash
   # Check versions
   pip list | grep -E "(numpy|pandas|scipy)"
   
   # Create fresh environment
   rm -rf .venv
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

### Platform-Specific Issues

#### macOS
```bash
# Install system dependencies
brew install python@3.11

# Fix SSL issues
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Windows
```bash
# Use PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Visual C++ build tools if needed
# Download from Microsoft Visual Studio
```

#### Linux
```bash
# Install system packages
sudo apt-get update
sudo apt-get install python3.11-dev python3.11-venv

# Fix permission issues
chmod +x examples/*.py
```

## Development Setup

### Pre-commit Hooks

Install git hooks for code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Code Formatting

Format code automatically:

```bash
# Format with black
black src/ tests/ examples/

# Sort imports
ruff check --fix src/ tests/ examples/
```

### Type Checking

Check type annotations:

```bash
# Run mypy
mypy src/

# Check specific file
mypy src/rpsd/denoise_robust.py
```

## Performance Considerations

### Memory Usage

- **Small datasets** (<10K points): 100-500MB RAM
- **Medium datasets** (10K-100K points): 500MB-2GB RAM
- **Large datasets** (>100K points): 2GB+ RAM

### Processing Speed

- **Wavelet denoising**: ~1000 points/second on modern hardware
- **Guardrail evaluation**: ~5000 points/second
- **Parameter search**: Depends on grid size and data length

### Optimization Tips

1. **Use appropriate wavelet levels**: More levels = slower but potentially better results
2. **Limit parameter search**: Smaller grids = faster optimization
3. **Process in chunks**: For very large datasets, consider windowing
4. **Use parallel processing**: Enable joblib parallelization when available

## Next Steps

After installation:

1. **Read the usage guide**: `docs/USAGE.md`
2. **Try the examples**: Run scripts in `examples/`
3. **Explore the API**: Check `src/rpsd/` for implementation details
4. **Run tests**: Ensure everything works correctly
5. **Check documentation**: Review `docs/` for advanced topics

## Support

For installation issues:

- Check the troubleshooting section above
- Review error messages carefully
- Check Python and package versions
- Open an issue on GitHub with system details
- Include error logs and environment information
