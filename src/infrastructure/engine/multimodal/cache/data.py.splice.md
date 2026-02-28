# Splice: src/infrastructure/engine/multimodal/cache/data.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MediaHash
- CacheEntry
- CacheStats
- PlaceholderRange

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
