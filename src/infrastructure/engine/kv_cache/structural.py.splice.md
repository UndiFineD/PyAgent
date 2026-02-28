# Splice: src/infrastructure/engine/kv_cache/structural.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- FreeBlockQueue
- BlockHashCache
- BlockPool

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
