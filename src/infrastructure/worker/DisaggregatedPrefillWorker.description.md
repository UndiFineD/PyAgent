# DisaggregatedPrefillWorker

**File**: `src\infrastructure\worker\DisaggregatedPrefillWorker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 155  
**Complexity**: 7 (moderate)

## Overview

Disaggregated Prefill Worker.

This module implements a specialized worker for the prefill stage of disaggregated inference.
In a disaggregated architecture, prefill workers focus on processing the input prompt and
generating the initial KV cache, which is then transferred to decode-only workers.

Optimized for:
- High compute throughput during prompt processing
- Efficient KV cache generation and serialization
- Background asynchronous transfer of KV blocks to remote consumers
- Massive context length handling through chunked prefill

Inspired by vLLM's specialized worker architectures.

## Classes (1)

### `DisaggregatedPrefillWorker`

Worker specialized in the prefill stage.

This worker handles the initial processing of requests. It does not perform
autoregressive decoding. Once the prefill is done, the KV cache is handed
off via a KVTransferConnector.

**Methods** (7):
- `__init__(self, worker_id, model_config, parallel_config, kv_transfer_config)`
- `initialize(self)`
- `execute_prefill(self, request)`
- `_optimize_prefill_overlap_rust(self, batch_metadata)`
- `handle_chunked_prefill(self, request, chunk_size)`
- `get_status(self)`
- `shutdown(self)`

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `logging`
- `src.core.lazy_loader.LazyLoader`
- `src.core.rust_bridge.RustBridge`
- `src.infrastructure.cache.KVCacheManager.DeviceType`
- `src.infrastructure.cache.KVCacheManager.KVCacheConfig`
- `src.infrastructure.cache.KVCacheManager.KVCacheManager`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorBase`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVConnectorRole`
- `src.infrastructure.kv_transfer.KVTransferConnector.KVTransferConfig`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 4 more

---
*Auto-generated documentation*
