# Splice: src/infrastructure/engine/pooling/strategies.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BasePooler
- MeanPooler
- CLSPooler
- LastTokenPooler
- MaxPooler
- AttentionPooler
- WeightedMeanPooler
- MatryoshkaPooler
- MultiVectorPooler
- StepPooler

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
