# Splice: src/infrastructure/storage/kv_transfer/k_vzap.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- KVzapConfig
- KVzapSurrogate
- KVzapPruner

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
