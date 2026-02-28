# Splice: src/infrastructure/engine/speculative/eagle/base.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- InputBuffer
- CpuGpuBuffer
- AttentionMetadata
- TreeAttentionMetadata

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
