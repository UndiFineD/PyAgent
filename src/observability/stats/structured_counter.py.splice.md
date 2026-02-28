# Splice: src/observability/stats/structured_counter.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StructuredCounter
- CompilationCounter
- RequestCounter
- CacheCounter
- PoolCounter
- QueueCounter

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
