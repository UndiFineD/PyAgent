# Splice: src/infrastructure/engine/kv_cache/context_sharder.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ContextShard
- ContextShardManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
