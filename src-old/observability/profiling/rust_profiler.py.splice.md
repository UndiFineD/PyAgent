# Splice: src/observability/profiling/rust_profiler.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- FunctionStats
- RustProfiler
- RustUsageScanner

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
