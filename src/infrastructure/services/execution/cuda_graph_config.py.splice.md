# Splice: src/infrastructure/services/execution/cuda_graph_config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CUDAGraphMode
- CUDAGraphConfig
- CUDAGraphEntry
- CUDAGraphRegistry
- CUDAGraphManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
