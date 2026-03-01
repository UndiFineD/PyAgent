# TensorParallelTransfer

**File**: `src\infrastructure\kv_transfer\TensorParallelTransfer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 90  
**Complexity**: 5 (moderate)

## Overview

Tensor-Parallel Aware KV Transfer.

In Tensor Parallelism (TP), KV heads (and thus KV cache blocks) are partitioned
across multiple GPUs within a single node or across nodes. This module ensures
that KV transfer logic correctly handles partitioned blocks, either by 
re-aggregating them for transfer or by performing parallel transfers of 
each shard.

Key Patterns:
- Sharded KV block transfer coordination
- All-to-all or All-gather patterns for KV metadata reconciliation
- Support for TP-aware PagedAttention block mapping
- Rust-accelerated bitmask aggregation for TP shards

## Classes (1)

### `TensorParallelTransfer`

Orchestrator for TP-aware KV transfer.

Handles the complexities of sharded KV caches where multiple TP ranks
must coordinate their independent transfers to respective TP ranks
in the destination group.

**Methods** (5):
- `__init__(self, tp_rank, tp_size, local_connector)`
- `_aggregate_tp_metadata_rust(self, metadata_shards)`
- `shard_aware_push(self, layer_name, kv_shard, attn_metadata)`
- `shard_aware_pull(self, layer_name, request_id)`
- `verify_tp_consistency(self, request_id)`

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
