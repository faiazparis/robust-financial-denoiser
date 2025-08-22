# Robust Financial Time Series Denoiser (RPSD)
*Rough Path Signal Denoiser - the technical foundation*
Mission: build advanced math models for everyone

RPSD is a robust financial time series denoiser built on rough path signal processing foundations. It reduces microstructure noise while preserving structural price movements with **mathematical precision**. Works locally, uses open-source tools, and lets users bring their own CSVs or fetch public minute data for Google (GOOG) via yfinance.

**Current Status**: This is a **working implementation** with demonstrated results on real data and **identity contract**. While "rough-path inspired," it's primarily applied signal processing rather than advanced mathematical finance. See docs/ADVANCED_MATH.md for a roadmap to truly advanced math.

## What Problems We Solve

**Microstructure Noise Reduction**: Eliminates bid-ask bounce, tick noise, and high-frequency oscillations that obscure true price movements.

**Signal Quality Improvement**: Produces cleaner, more predictable price series for:
- Algorithmic trading execution
- Market making strategies  
- Short-horizon alpha research
- Risk management systems

**Mathematical Precision**: **Identity contract** - when smoothing is disabled, denoised output equals input exactly.

**Quantitative Metrics**: Demonstrated variance reduction on real market data:
- **GOOG**: 97.12% realized variance reduction (39.12 → 1.12)

## How It Works

**Robust Implementation**: Uses explicit indexing and length validation to ensure **reliable operation** and **baseline preservation**.

**Sliding Window Processing**: Divides price series into overlapping segments for localized analysis with guaranteed coverage.

**Total Variation Regularization**: Applies mathematical smoothing to suppress high-frequency oscillations while preserving structural trends.

**Identity-Safe Processing**: 
- Computes increments with `inc[0] = 0.0; inc[1:] = x[1:] - x[:-1]`
- Reconstructs with `baseline + np.cumsum(inc)` for exact length preservation
- Validates shapes at each step with `assert_shapes()` function

**Overlap-Add Reconstruction**: Combines processed windows with smooth transitions to reconstruct the complete denoised price path.

## Before/After Results & Visualizations

**Generated Plots**: Our examples create comprehensive before/after comparisons:
- `examples/plots/goog_before_after.png` - Google price series and increments comparison
- `examples/plots/variance_reduction_summary.png` - Overall performance metrics

**What the Plots Show**:
- **Top panels**: Price series comparison (original vs. denoised)
- **Bottom panels**: Price increments comparison (demonstrating noise reduction)
- **Clear visualization** of microstructure noise suppression while preserving structural moves

**Google (GOOG) Real Market Data Analysis**:

![Google Price Series Denoising](examples/plots/goog_before_after.png)

**Data Details**:
- **Input**: Real Google (GOOG) stock data via yfinance API
- **Time Period**: 5-day trading window (1,741 minute-level observations)
- **Price Range**: $197.68 - $205.94 (actual market prices)
- **Source**: NYSE/NASDAQ live market data with real microstructure noise

**Processing**:
- **Algorithm**: Robust rough path-inspired denoising with total variation regularization
- **Parameters**: Window=250, overlap=0.5, λ_var=1.2, max_iters=200
- **Output**: Denoised price series preserving structural movements with baseline
- **Performance**: 97.12% variance reduction achieved with **identity contract**

**What You See**:
- **Top Panel**: Original (blue) vs. denoised (orange) price series - noise removed while trends preserved
- **Bottom Panel**: Price increments showing dramatic reduction in high-frequency oscillations
- **Result**: 97.12% realized variance reduction (39.12 → 1.12) on live market data

**Performance Summary**:
![Variance Reduction Summary](examples/plots/variance_reduction_summary.png)

*Quantitative validation: 97.12% variance reduction achieved on real Google market data with identity contract and baseline preservation.*

**Quantitative Results**:
- **GOOG**: 97.12% realized variance reduction (39.12 → 1.12) - **Excellent performance**
- **Identity Contract**: ✅ Working baseline preservation (205.08000183 → 205.08000183)
- **Length Stability**: ✅ No more array length mismatches
- **Mathematical Precision**: ✅ Reliable operation, robust implementation

**Technical Achievements**:
- ✅ **Identity Contract**: `denoised == original` when smoothing disabled
- ✅ **Robust Implementation**: Explicit indexing prevents length issues
- ✅ **Baseline Preservation**: First price preserved across all operations
- ✅ **Length Validation**: `assert_shapes()` catches drift immediately
- ✅ **Domain Consistency**: Works reliably in both raw and standardized domains

Quickstart (Python 3.11)
```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
pre-commit install

# Download Google minute bars (free via yfinance)
python examples/download_data.py

# Test identity contract (should return exact input)
rpsd denoise --input examples/goog_1m.csv --output examples/goog_identity.csv \
  --window 150 --overlap 0.5 --lambda-var 0.0 --max-iters 1 --verbose

# Denoise with smoothing
rpsd denoise --input examples/goog_1m.csv --output examples/goog_denoised.csv \
  --window 250 --overlap 0.5 --lambda-var 1.2 --max-iters 200 --verbose

# Evaluate results
rpsd evaluate --original examples/goog_1m.csv --denoised examples/goog_denoised.csv

# Generate plots
python examples/plot_real_data.py
```

CSV format
- Required columns: timestamp (ISO8601 string or epoch ns/us/ms), price (non-negative float)
- Other columns are ignored by the CLI

Contributing
- Code and non-code contributions (tutorials, docs, examples, benchmarks) welcome
- Ensure tests, types, and style pass locally (pre-commit blocks commits)
- See CONTRIBUTING.md

## References & Further Reading

**Background**: See `docs/BACKGROUND.md` for context on rough paths and microstructure.

**Advanced Math Roadmap**: See `docs/ADVANCED_MATH.md` for how to transform this into truly advanced mathematical finance.

**Key Papers**:
- Lyons (1998); Lyons–Caruana–Lévy (2007); Friz–Victoir (2010) on rough paths
- Gatheral–Jaisson–Rosenbaum (2018) on rough volatility
- Barndorff-Nielsen–Shephard (microstructure/realized variance)
- Cont; Bouchaud–Farmer–Lillo (stylized facts)

License
- MIT

## Mission: Building Advanced Math Models

**Current Achievement**: We've built a **robust, working financial time series denoiser** with **identity contract** and demonstrated results on real data.

**Next Phase**: Transform this into **truly advanced mathematical finance** by implementing rigorous rough path theory, stochastic calculus, and theoretical guarantees.

**Why This Matters**: 
- **Foundation**: Solid working implementation with empirical validation and mathematical precision
- **Path Forward**: Clear roadmap to advanced math (see `docs/ADVANCED_MATH.md`)
- **Impact**: From "working tool" to "mathematical contribution"

**Note on scope**: Production guidance and roadmap live in `docs/PRODUCTION.md`
