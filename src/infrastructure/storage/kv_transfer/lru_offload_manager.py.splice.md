# Splice: src/infrastructure/storage/kv_transfer/lru_offload_manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- LRUEntry
- LRUOffloadManager
- WeightedLRUManager
- TieredLRUManager
- PrefetchingLRUManager
- AsyncLRUManager
- LRUManagerFactory

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
