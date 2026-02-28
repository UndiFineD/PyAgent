# Splice: src/infrastructure/engine/scheduling/chunked_prefill/types.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ChunkState
- ChunkPriority
- ChunkMetrics
- PrefillChunk
- ChunkedRequest
- ChunkedPrefillConfig

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
