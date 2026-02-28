# Splice: src/observability/stats/engine.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ObservabilityCore
- ObservabilityEngine
- StatsCore
- StatsNamespaceManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
