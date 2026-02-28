# Splice: src/infrastructure/services/dev/scripts/analysis/run_profiled_self_improvement.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RustFunctionStats
- RustProfiler
- ComprehensiveProfileAnalyzer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
