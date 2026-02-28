# Splice: src/observability/stats/compilation_counter.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CompileEventType
- CompileEvent
- FunctionStats
- CompilationCounter
- RecompileTracker
- TrendAnalyzer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
