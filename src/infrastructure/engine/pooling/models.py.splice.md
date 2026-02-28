# Splice: src/infrastructure/engine/pooling/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- PoolingTask
- PoolingStrategy
- PoolingConfig
- PoolingResult
- EmbeddingOutput
- ClassificationOutput

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
