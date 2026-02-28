# Splice: src/infrastructure/compute/cuda/cuda_graph_manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- CUDAGraphMode
- BatchDescriptor
- CUDAGraphEntry
- CUDAGraphOptions
- CUDAGraphStats
- MockCUDAGraph
- CUDAGraphWrapper
- AdaptiveCUDAGraphWrapper

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
