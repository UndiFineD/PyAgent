# Splice: src/observability/stats/request_metrics.py

This module contains multiple types that are logically distinct:

- `RequestState` (Enum): request lifecycle states.
- `RequestMetrics` (dataclass): timing and counters for a single request.

Suggested splices:
- `types.py`: keep `RequestState` and other small enums.
- `metrics.py`: keep `RequestMetrics` and related helper functions for timing.
