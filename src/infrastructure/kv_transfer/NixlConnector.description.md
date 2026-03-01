# NixlConnector

**File**: `src\infrastructure\kv_transfer\NixlConnector.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 24 imports  
**Lines**: 230  
**Complexity**: 10 (moderate)

## Overview

NIXL High-Performance KV Transfer Connector.

NIXL (Network Interconnect for X-Large models) provides a low-latency, high-bandwidth
transport layer for KV cache blocks between disaggregated prefill and decode instances.
It utilizes RDMA techniques and peer-to-peer memory copies to minimize CPU overhead.

Inspired by vLLM's NixlConnector and advanced distributed communication patterns.

## Classes (3)

### `NixlMemoryRegionStatus`

**Inherits from**: IntEnum

Status of an RDMA memory region.

### `NixlMemoryRegion`

Represents a registered memory region for RDMA operations.

### `NixlConnector`

**Inherits from**: KVConnectorBase

NIXL high-performance connector logic.

**Methods** (10):
- `__init__(self, config, kv_cache_config)`
- `_init_rdma(self)`
- `_poll_loop(self)`
- `register_memory(self, tensor)`
- `transfer_blocks(self, target_rank, block_ids, local_tensor, remote_buffer_ptr, rkey)`
- `poll_completions(self)`
- `start_load_kv(self, forward_context)`
- `wait_for_layer_load(self, layer_name)`
- `save_kv_layer(self, layer_name, kv_layer, attn_metadata)`
- `close(self)`

## Dependencies

**Imports** (24):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.IntEnum`
- `logging`
- `numpy`
- `src.core.lazy_loader.LazyLoader`
- `src.core.rust_bridge.RustBridge`
- `src.infrastructure.kv_transfer.KVTransferConnector.ForwardContext`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorBase`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorMetadata`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorRole`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVTransferConfig`
- `threading`
- `time`
- ... and 9 more

---
*Auto-generated documentation*
