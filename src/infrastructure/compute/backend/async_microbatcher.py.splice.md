# Splice: src/infrastructure/compute/backend/async_microbatcher.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BatchItem
- BatchStats
- AsyncMicrobatcher
- SyncMicrobatcher

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
