# PipelineParallelTransfer

**File**: `src\infrastructure\kv_transfer\PipelineParallelTransfer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 95  
**Complexity**: 5 (moderate)

## Overview

Pipeline-Parallel Aware KV Transfer.

This module provides orchestration for KV cache transfers when Pipeline Parallelism (PP)
is enabled. In PP scenarios, different layers of the model reside on different pipeline
stages (processes/nodes). KV transfer must be coordinated such that each stage's 
respective KV blocks are transferred to the correct corresponding stages in the 
destination (prefill -> decode) group.

Key Patterns:
- Stage-to-stage mapping for disaggregated PP
- Synchronized collective transfers for KV metadata
- Latency hiding by overlapping PP stage transfers
- Rust-accelerated PP stage mapping logic

## Classes (1)

### `PipelineParallelTransfer`

Orchestrator for PP-aware KV transfer.

Coordinates multiple KV connectors across pipeline stages to ensure
consistent transfer of a request's full KV context.

**Methods** (5):
- `__init__(self, pp_rank, pp_size, local_connector)`
- `_calculate_pp_stage_mapping_rust(self, num_layers, pp_size)`
- `coordinate_transfer_start(self, request_id, metadata)`
- `sync_stage_transfer(self, layer_idx)`
- `get_stage_status(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `src.core.lazy_loader.LazyLoader`
- `src.core.rust_bridge.RustBridge`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorBase`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`
- `typing.Tuple`

---
*Auto-generated documentation*
