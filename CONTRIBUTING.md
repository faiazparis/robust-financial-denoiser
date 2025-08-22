# Contributing Guidelines

## Welcome Contributors!

We welcome contributions that improve the Robust Financial Time Series Denoiser. This project aims to build **working, reliable tools** with **transparent capabilities** and **clear limitations**.

## What We're Building

**Current Status**: A robust financial time series denoiser with fidelity-first metrics and comprehensive guardrails.

**Goal**: Transform this into truly advanced mathematical finance through rigorous implementation and theoretical development.

**Philosophy**: 
- **Transparency over perfection**: Clear about what works and what doesn't
- **Fidelity over performance**: Signal preservation beats aggressive noise removal
- **Validation over claims**: Demonstrated results over marketing language
- **Iterative improvement**: Small, tested changes over big promises

## Areas for Contribution

### High Priority

1. **Signal Fidelity Improvements**
   - Better guardrail metrics
   - More robust denoising algorithms
   - Improved parameter optimization

2. **Performance Validation**
   - Comprehensive testing on diverse datasets
   - Cross-asset validation
   - Long-term stability testing

3. **Documentation Clarity**
   - Clear usage examples
   - Honest capability descriptions
   - Transparent limitation documentation

### Medium Priority

1. **Code Quality**
   - Type annotation improvements
   - Error handling enhancements
   - Performance optimizations

2. **Testing Coverage**
   - Edge case testing
   - Integration testing
   - Performance benchmarking

3. **User Experience**
   - Better error messages
   - Improved CLI interface
   - Configuration management

### Low Priority

1. **Advanced Features**
   - Real-time processing
   - Web interface
   - Database integration

2. **Optimization**
   - GPU acceleration
   - Distributed processing
   - Memory optimization

## Contribution Guidelines

### Code Standards

1. **Type Annotations**: Use explicit types for all functions
2. **Documentation**: Clear docstrings explaining purpose and limitations
3. **Testing**: Write tests for new functionality
4. **Style**: Follow black and ruff formatting

### Documentation Standards

1. **Honest Claims**: Don't overpromise capabilities
2. **Clear Limitations**: Document what doesn't work
3. **Real Examples**: Use actual results, not theoretical best cases
4. **Transparent Metrics**: Show both successes and failures

### Testing Requirements

1. **Unit Tests**: Cover new functionality
2. **Integration Tests**: Test with real data
3. **Performance Tests**: Benchmark against baselines
4. **Regression Tests**: Ensure existing functionality works

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/faiazparis/robust-financial-denoiser.git
cd robust-financial-denoiser

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### 2. Create Feature Branch

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Ensure branch is up to date
git pull origin main
```

### 3. Make Changes

1. **Code Changes**: Implement your feature
2. **Tests**: Write comprehensive tests
3. **Documentation**: Update relevant docs
4. **Type Checking**: Ensure mypy passes

### 4. Quality Checks

```bash
# Run all quality checks
pre-commit run --all-files

# Run tests
pytest tests/ -v

# Type checking
mypy src/

# Linting
ruff check src/ tests/
```

### 5. Commit and Push

```bash
# Add changes
git add .

# Commit with clear message
git commit -m "Add feature: brief description"

# Push to remote
git push origin feature/your-feature-name
```

### 6. Create Pull Request

1. **Title**: Clear, descriptive title
2. **Description**: Explain what and why, not just what
3. **Testing**: Describe how you tested
4. **Limitations**: Note any known issues or limitations

## Code Review Process

### What We Look For

1. **Functionality**: Does it work as intended?
2. **Quality**: Is the code well-written and tested?
3. **Documentation**: Are changes clearly documented?
4. **Limitations**: Are limitations honestly stated?
5. **Testing**: Is functionality properly validated?

### Review Guidelines

1. **Be Constructive**: Focus on improvement, not criticism
2. **Ask Questions**: Understand the reasoning behind choices
3. **Suggest Alternatives**: Offer concrete suggestions
4. **Check Claims**: Verify that claims are supported by evidence

## Testing Guidelines

### Test Data

1. **Real Data**: Use actual financial data when possible
2. **Synthetic Data**: Create realistic synthetic data for edge cases
3. **Diverse Assets**: Test across different market instruments
4. **Time Periods**: Test across different market conditions

### Test Metrics

1. **Functionality**: Does it produce expected outputs?
2. **Performance**: Does it meet performance requirements?
3. **Robustness**: Does it handle edge cases gracefully?
4. **Regression**: Does it maintain existing functionality?

### Test Documentation

1. **Test Purpose**: What is being tested and why?
2. **Test Data**: What data is used and why?
3. **Expected Results**: What should happen?
4. **Actual Results**: What actually happened?

## Documentation Guidelines

### Writing Style

1. **Clear and Concise**: Simple, direct language
2. **Honest Claims**: Don't overpromise or oversell
3. **Real Examples**: Use actual results, not theoretical best cases
4. **Clear Limitations**: Document what doesn't work

### Content Requirements

1. **Purpose**: What does this do?
2. **Usage**: How do you use it?
3. **Limitations**: What are the known limitations?
4. **Examples**: Real, working examples
5. **Troubleshooting**: Common issues and solutions

### Review Process

1. **Technical Accuracy**: Is the information correct?
2. **Clarity**: Is it easy to understand?
3. **Completeness**: Does it cover necessary topics?
4. **Honesty**: Are claims supported by evidence?

## Issue Reporting

### Bug Reports

1. **Clear Description**: What went wrong?
2. **Reproduction Steps**: How can we reproduce it?
3. **Expected Behavior**: What should have happened?
4. **Actual Behavior**: What actually happened?
5. **Environment**: System details and versions

### Feature Requests

1. **Problem Statement**: What problem does this solve?
2. **Proposed Solution**: How should it work?
3. **Use Cases**: When would this be useful?
4. **Alternatives**: What alternatives exist?

### Enhancement Requests

1. **Current Limitation**: What's currently limiting?
2. **Proposed Improvement**: How should it be improved?
3. **Impact**: What's the expected benefit?
4. **Effort Estimate**: How much work is involved?

## Community Guidelines

### Communication

1. **Respectful**: Treat others with respect
2. **Constructive**: Focus on building, not tearing down
3. **Honest**: Be truthful about capabilities and limitations
4. **Helpful**: Offer assistance when possible

### Collaboration

1. **Open Discussion**: Welcome different viewpoints
2. **Evidence-Based**: Support claims with evidence
3. **Iterative Improvement**: Build on existing work
4. **Shared Learning**: Share knowledge and insights

## Recognition

### Contributor Recognition

1. **Code Contributors**: Listed in contributors file
2. **Documentation Contributors**: Acknowledged in docs
3. **Testing Contributors**: Recognized for quality improvements
4. **Community Contributors**: Appreciated for community building

### Contribution Types

1. **Code**: Implementation and bug fixes
2. **Documentation**: Guides and examples
3. **Testing**: Test cases and validation
4. **Community**: Support and outreach
5. **Research**: Theoretical contributions

## Getting Help

### Questions and Support

1. **GitHub Issues**: For bugs and feature requests
2. **Discussions**: For questions and ideas
3. **Documentation**: Check existing docs first
4. **Examples**: Review working examples

### Learning Resources

1. **Code Examples**: Working implementations
2. **Documentation**: Comprehensive guides
3. **Tests**: Examples of expected behavior
4. **Issues**: Common problems and solutions

## Final Notes

### Our Commitment

1. **Transparency**: Honest about capabilities and limitations
2. **Quality**: Focus on working, reliable tools
3. **Community**: Welcome diverse contributions
4. **Learning**: Continuous improvement through feedback

### Your Impact

Every contribution, no matter how small, helps build better tools for everyone. Whether it's fixing a typo, improving documentation, or implementing new features, your work makes a difference.

Thank you for contributing to building advanced mathematical tools for everyone!
