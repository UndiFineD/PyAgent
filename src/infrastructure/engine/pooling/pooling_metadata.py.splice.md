# Splice: src/infrastructure/engine/pooling/pooling_metadata.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- PoolingStrategy
- PoolingCursor
- PoolingStates
- PoolingMetadata
- Pooler
- MeanPooler
- MaxPooler
- LastTokenPooler
- AttentionWeightedPooler
- PoolerFactory
- PoolerOutput
- ChunkedPoolingManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
