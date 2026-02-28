# Splice: src/infrastructure/services/execution/input_batch.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- SamplingMetadata
- InputBuffers
- InputBatch
- BatchBuilder

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
