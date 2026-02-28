# Splice: src/observability/stats/metrics_engine.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ObservabilityEngine
- TokenCostEngine
- ModelFallbackEngine

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
