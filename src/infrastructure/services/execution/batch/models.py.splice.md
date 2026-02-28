# Splice: src/infrastructure/services/execution/batch/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MoveDirectionality
- CachedRequestState
- BatchUpdateBuilder
- SamplingMetadata
- InputBatch

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
