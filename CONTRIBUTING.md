# Contributing

We welcome code and non-code PRs (tutorials, docs, examples, benchmarks) to help build advanced math models for everyone.

## Project Status

**Current Achievement**: We've built a **robust financial time series denoiser** with **identity contract** and **mathematical precision**.

**Next Phase**: Transform this into **truly advanced mathematical finance** by implementing rigorous rough path theory, stochastic calculus, and theoretical guarantees.

## Contribution Areas

### Code Contributions
- **Core Algorithms**: Improve TV proximal, add new regularization methods
- **Advanced Math**: Implement rough path signatures, stochastic calculus
- **Performance**: Optimize window processing, add parallelization
- **Testing**: Add comprehensive test coverage, edge case handling

### Non-Code Contributions
- **Documentation**: Improve mathematical explanations, add examples
- **Tutorials**: Create guides for different use cases
- **Benchmarks**: Compare with other denoising methods
- **Research**: Explore theoretical foundations, mathematical proofs

## Quality Standards

### Code Quality
- ✅ **Tests must pass**: Run `pytest -q` before submitting
- ✅ **Types must pass**: Run `mypy src` for type checking
- ✅ **Style must pass**: Run `ruff check src` for linting
- ✅ **Identity contract**: Ensure `denoised == original` when `lambda-var=0.0`

### Mathematical Precision
- ✅ **Baseline preservation**: First price must be preserved exactly
- ✅ **Length stability**: No array length mismatches
- ✅ **Domain consistency**: Works in both raw and standardized domains
- ✅ **Reliable operation**: All operations must complete without errors

### Documentation
- ✅ **Update docs**: Document user-facing changes
- ✅ **Mathematical clarity**: Explain algorithms and their properties
- ✅ **Examples**: Provide working code examples
- ✅ **References**: Cite relevant mathematical literature

## Development Workflow

### Before Contributing
1. **Verify current status**: Run identity tests to ensure system is working
   ```bash
   python -c "from src.rpsd.denoise import test_identity_contract; test_identity_contract()"
   ```
2. **Check project state**: Ensure all existing tests pass
   ```bash
   pytest -q
   mypy src
   ruff check src
   ```

### Making Changes
1. **Small, focused changes**: Prefer incremental improvements
2. **Test thoroughly**: Add tests for new functionality
3. **Maintain identity contract**: Ensure mathematical precision is preserved
4. **Document changes**: Update relevant documentation

### Testing Your Changes
1. **Identity contract**: Verify `lambda-var=0.0` returns exact input
2. **Baseline preservation**: Check first price is preserved exactly
3. **Length stability**: Ensure no array length mismatches
4. **Real data**: Test on actual market data (e.g., Google data)

## Key Principles

1. **Mathematical Precision**: Every change must preserve the identity contract
2. **Robust Implementation**: Reliable operation, length preservation
3. **Real Data Validation**: Theoretical methods must work on actual data
4. **Progressive Enhancement**: Build on the solid foundation we've created

## Getting Started

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Run all tests**: `pytest -q && mypy src && ruff check src`
5. **Test identity contract**: Ensure mathematical precision is maintained
6. **Submit a PR** with clear description of changes

## Questions?

- **Mathematical**: Check `docs/ADVANCED_MATH.md` for roadmap
- **Implementation**: Review `docs/BACKGROUND.md` for current status
- **Usage**: See `docs/USAGE.md` for examples
- **Production**: Check `docs/PRODUCTION.md` for deployment guidance

**Together, we can build advanced math models that work reliably in the real world!** 🚀
