# PyAgent Fleet Loop Analysis Tool

A reusable utility for detecting loop anti-patterns and performance bottlenecks across the PyAgent fleet.

## Overview

This tool analyzes Python files for potential performance issues related to excessive loop usage, nesting, and complexity. It uses ripgrep for fast pattern matching and provides detailed metrics for prioritizing optimization efforts.

## Features

- **Fast Analysis**: Uses ripgrep for high-performance loop detection
- **Comprehensive Metrics**: LOC, loop count, density, complexity scoring
- **Nesting Detection**: Identifies nested and deeply nested loops
- **Configurable Thresholds**: Customizable analysis parameters
- **Multiple Output Formats**: Summary, detailed, and JSON formats
- **Fleet-Compatible**: Designed for reuse across multiple projects

## Usage

### Basic Usage

```bash
# Analyze current directory
python loop_analysis.py .

# Analyze specific directory
python loop_analysis.py src/core/

# Analyze external repository
python loop_analysis.py 
```

### Advanced Options

```bash
# Custom thresholds
python loop_analysis.py src/ --min-loc 100 --min-loops 2

# Exclude additional directories
python loop_analysis.py . --exclude .venv __pycache__ node_modules .git target build

# Detailed output with top files analysis
python loop_analysis.py src/ --format detailed

# JSON output for integration
python loop_analysis.py src/ --format json --output results.json

# Quiet mode (no progress messages)
python loop_analysis.py src/ --quiet
```

## Metrics Explained

- **LOC**: Lines of code
- **Loops**: Number of for/while statements
- **Density**: Loops per 100 lines of code
- **Score**: Complexity score (higher = more optimization priority)
- **Flags**:
  - `NESTED`: Contains nested loops
  - `DEEP`: Nesting > 3 levels
  - `LARGE`: Contains loops with > 50 statements

## Integration

### As a Module

```python
from src.core.specialists.loop_analyzer import LoopAnalyzer, LoopAnalysisConfig

config = LoopAnalysisConfig(
    min_loc_threshold=200,
    min_loop_threshold=3,
    exclude_dirs={'.venv', '__pycache__'}
)

analyzer = LoopAnalyzer(config)
results = analyzer.find_candidates('src/')
```

### In CI/CD Pipelines

```yaml
# .github/workflows/loop-analysis.yml
name: Loop Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Loop Analysis
        run: python loop_analysis.py src/ --format json --output loop-report.json
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: loop-analysis-report
          path: loop-report.json
```

## Configuration

### Default Settings

- **Min LOC**: 200 lines
- **Min Loops**: 3 loops
- **Excluded Dirs**: `.venv`, `__pycache__`, `node_modules`, `.git`, `target`, `build`
- **File Patterns**: `*.py`

### Custom Configuration

```python
from src.core.specialists.loop_analyzer import LoopAnalysisConfig

config = LoopAnalysisConfig(
    min_loc_threshold=500,      # Only analyze large files
    min_loop_threshold=5,       # Require more loops
    exclude_dirs={'dist', 'build', 'temp'},
    include_patterns=['*.py', '*.pyx'],  # Include Cython files
    exclude_patterns=['test_*', '*_test.py']  # Exclude test files
)
```

## Performance Optimization Targets

Based on analysis, prioritize files with:

1. **High Complexity Score** (>300): Critical optimization targets
2. **Deep Nesting**: Refactor to reduce nesting levels
3. **High Loop Density** (>10%): Consider algorithmic improvements
4. **Large Loops**: Break down into smaller, focused functions

## Examples

### High Priority Files (Score > 400)

These files should be prioritized for optimization:

```
src/core/base/logic/core/active_directory_analysis_core.py
- LOC: 810, Loops: 78, Density: 9.6%, Score: 492.3 [NESTED, DEEP]
```

### Optimization Strategies

1. **Replace loops with vectorized operations** (NumPy, Pandas)
2. **Use list/dict comprehensions** for simple transformations
3. **Implement caching** for repeated computations
4. **Consider async/parallel processing** for I/O bound loops
5. **Break large functions** into smaller, focused units

## Contributing

When adding new analysis features:

1. Update the `LoopAnalysisResult` dataclass for new metrics
2. Add analysis methods to `LoopAnalyzer` class
3. Update the CLI interface in `loop_analysis.py`
4. Add tests for new functionality
5. Update this documentation

## License

Copyright 2026 PyAgent Authors. Licensed under Apache 2.0.