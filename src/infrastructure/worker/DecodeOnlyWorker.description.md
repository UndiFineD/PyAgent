# DecodeOnlyWorker

**File**: `src\infrastructure\worker\DecodeOnlyWorker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 143  
**Complexity**: 6 (moderate)

## Overview

Decode-Only Worker.

This module implements a specialized worker for the decode stage of disaggregated inference.
Decode-only workers receive KV cache from prefill workers and perform low-latency, 
autoregressive token generation.

Optimized for:
- Low-latency token-by-token generation
- Efficient incremental KV cache loading from remote producers
- Minimal memory footprint (swapping unused KV blocks to remote storage)
- High concurrency for many concurrent sequences

Inspired by vLLM's specialized worker architectures and disaggregated prefill-decode patterns.

## Classes (1)

### `DecodeOnlyWorker`

Worker specialized in the decode stage.

This worker assumes the prefill (initial prompt processing) has been done elsewhere.
It pulls the necessary KV cache blocks on-demand or ahead-of-time from the 
distributed pool (e.g., Mooncake) and proceeds with generation.

**Methods** (6):
- `__init__(self, worker_id, model_config, parallel_config, kv_transfer_config)`
- `initialize(self)`
- `execute_step(self, active_requests)`
- `_schedule_kv_prefetch_rust(self, seq_metadata)`
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
