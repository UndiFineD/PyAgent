# Splice: src/infrastructure/engine/sampling/kernels.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- TemperatureSampler
- TopKSampler
- TopPSampler
- TopKTopPSampler
- GumbelSampler
- RepetitionPenaltySampler
- PenaltySampler

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
