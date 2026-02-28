# Splice: src/observability/stats/alerting.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ThresholdAlertManager
- RetentionEnforcer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
