# Splice: src/infrastructure/engine/attention/backend/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AttentionBackendEnum
- AttentionType
- AttentionCapabilities
- AttentionMetadata

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
