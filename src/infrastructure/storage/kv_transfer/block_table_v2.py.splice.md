# Splice: src/infrastructure/storage/kv_transfer/block_table_v2.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- BlockAllocationStrategy
- BlockTableConfig
- BlockInfo
- CpuGpuBuffer
- BlockTable
- SparseBlockTable
- PredictiveBlockAllocator
- DistributedBlockTable
- BlockTableV2
- BlockTableFactory

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
