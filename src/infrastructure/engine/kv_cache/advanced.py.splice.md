# Splice: src/infrastructure/engine/kv_cache/advanced.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- HierarchicalKVCacheCoordinator
- PredictiveKVCacheCoordinator
- AsyncPrefetchCoordinator

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
