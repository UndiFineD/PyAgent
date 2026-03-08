# Splice: src/observability/stats/ab_engine.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ABComparisonResult
- ABSignificanceResult
- ABComparison
- ABComparisonEngine
- ABComparator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
