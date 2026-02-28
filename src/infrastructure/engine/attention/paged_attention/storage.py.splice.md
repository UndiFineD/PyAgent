# Splice: src/infrastructure/engine/attention/paged_attention/storage.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BlockTable
- SlotMapping
- PagedKVCache
- AttentionMetadata

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
