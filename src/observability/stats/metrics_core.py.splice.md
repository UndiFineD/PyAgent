# Splice: src/observability/stats/metrics_core.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TokenCostResult
- TokenCostCore
- ModelFallbackCore
- DerivedMetricCalculator
- StatsRollupCore
- CorrelationCore
- ABTestCore

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
