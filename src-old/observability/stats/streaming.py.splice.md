# Splice: src/observability/stats/streaming.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StatsStream
- StatsStreamManager
- StatsStreamer

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
