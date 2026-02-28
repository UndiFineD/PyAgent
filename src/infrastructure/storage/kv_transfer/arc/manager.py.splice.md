# Splice: src/infrastructure/storage/kv_transfer/arc/manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ARCOffloadManager
- AdaptiveARCManager
- AsyncARCManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
