# MooncakeConnector

**File**: `src\infrastructure\kv_transfer\MooncakeConnector.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 27 imports  
**Lines**: 358  
**Complexity**: 13 (moderate)

## Overview

Mooncake KV Transfer Connector.

This module implements the Mooncake-style KV transfer protocol for datacenter-scale inference.
Mooncake is a KVCache-centric disaggregated inference architecture that separates prefill
and decode nodes, using a distributed KV cache system as a shared buffer.

Inspired by the "Mooncake: A KVCache-centric Disaggregated Low-latency LLM Serving System" 
research and vLLM's implementation patterns.

Key Features:
- Distributed KV cache orchestration
- Asynchronous RDMA-based (simulated/pluggable) transfers
- Metadata-driven routing for prefill-to-decode handover
- Support for chunked prefill and incremental loading
- Rust-accelerated buffer management

## Classes (3)

### `MooncakeTransferStatus`

**Inherits from**: Enum

Status of a Mooncake KV transfer operation.

### `MooncakeRemoteTarget`

Represents a remote Mooncake node for KV storage or retrieval.

### `MooncakeConnector`

**Inherits from**: KVConnectorBase

Mooncake-style KV transfer connector.

Implements a distributed KV cache pool where prefill workers (producers)
push computed KV blocks, and decode workers (consumers) pull them.

This connector uses Rust acceleration for:
- Block serialization/deserialization
- Checksum validation
- Buffer memory management

**Methods** (13):
- `__init__(self, config, kv_cache_config)`
- `_mooncake_transfer_rust(self, data, target, mode)`
- `_verify_checksum_rust(self, buffer)`
- `start_load_kv(self, forward_context)`
- `wait_for_layer_load(self, layer_name)`
- `save_kv_layer(self, layer_name, kv_layer, attn_metadata)`
- `wait_for_save(self)`
- `_identify_remote_blocks(self, attn_metadata)`
- `_initiate_async_pull(self, request_id, block_id, node_id)`
- `_initiate_async_push(self, request_id, layer_name, kv_layer, attn_metadata)`
- ... and 3 more methods

## Dependencies

**Imports** (27):
- `__future__.annotations`
- `collections`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `numpy`
- `src.core.lazy_loader.LazyLoader`
- `src.core.rust_bridge.RustBridge`
- `src.infrastructure.cache.KVCacheManager.DeviceType`
- `src.infrastructure.kv_transfer.KVTransferConnector.ForwardContext`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVCacheBlocks`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorBase`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorMetadata`
- ... and 12 more

---
*Auto-generated documentation*
