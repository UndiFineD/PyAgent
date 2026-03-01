# decode_bench

**File**: `src\infrastructure\kv_transfer\connector\decode_bench.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 190  
**Complexity**: 11 (moderate)

## Overview

Phase 45: Decode Bench KV Connector
KV Connector for decode instance benchmarking.

## Classes (1)

### `DecodeBenchConnector`

**Inherits from**: KVConnectorBase

KV Connector for decode instance benchmarking.

**Methods** (11):
- `__init__(self, config, kv_cache_config)`
- `_init_group_mapping(self)`
- `start_load_kv(self, forward_context)`
- `_start_fill_kv(self, metadata)`
- `_fill_blocks(self, group_idx, block_ids, num_tokens)`
- `wait_for_layer_load(self, layer_name)`
- `save_kv_layer(self, layer_name, kv_layer, attn_metadata)`
- `get_num_new_matched_tokens(self, request, num_computed_tokens)`
- `update_state_after_alloc(self, request, blocks, num_external_tokens)`
- `build_connector_meta(self, scheduler_output)`
- ... and 1 more methods

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `logging`
- `src.infrastructure.kv_transfer.connector.base.KVConnectorBase`
- `src.infrastructure.kv_transfer.connector.types.ForwardContext`
- `src.infrastructure.kv_transfer.connector.types.KVCacheBlocks`
- `src.infrastructure.kv_transfer.connector.types.KVConnectorMetadata`
- `src.infrastructure.kv_transfer.connector.types.KVTransferConfig`
- `src.infrastructure.kv_transfer.connector.types.Request`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`
- `typing.Tuple`

---
*Auto-generated documentation*
