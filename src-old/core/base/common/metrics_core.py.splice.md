# Splice: src/core/base/common/metrics_core.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MetricRecord
- AgentMetrics
- MetricsCore

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
