# Splice: src/infrastructure/services/tools/table_cache.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TableMetadata
- TableTrieNode
- TableCacheManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
