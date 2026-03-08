# Splice: src/core/base/logic/structures/staged_batch_writer.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- WritePolicy
- CoalesceStrategy
- StagedWrite
- WriteStats
- StagedBatchWriter
- StagedWriteTensor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
