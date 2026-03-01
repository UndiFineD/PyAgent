# base

**File**: `src\infrastructure\kv_transfer\connector\base.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 110  
**Complexity**: 14 (moderate)

## Overview

Phase 45: KV Transfer Connector Base
Abstract base class for all KV transfer connectors.

## Classes (1)

### `KVConnectorBase`

**Inherits from**: ABC

Abstract base class for KV transfer connectors.

**Methods** (14):
- `__init__(self, config, kv_cache_config)`
- `register_kv_caches(self, kv_caches)`
- `start_load_kv(self, forward_context)`
- `wait_for_layer_load(self, layer_name)`
- `save_kv_layer(self, layer_name, kv_layer, attn_metadata)`
- `wait_for_save(self)`
- `get_num_new_matched_tokens(self, request, num_computed_tokens)`
- `update_state_after_alloc(self, request, blocks, num_external_tokens)`
- `build_connector_meta(self, scheduler_output)`
- `request_finished(self, request, block_ids)`
- ... and 4 more methods

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `src.infrastructure.kv_transfer.connector.types.ForwardContext`
- `src.infrastructure.kv_transfer.connector.types.KVCacheBlocks`
- `src.infrastructure.kv_transfer.connector.types.KVConnectorMetadata`
- `src.infrastructure.kv_transfer.connector.types.KVTransferConfig`
- `src.infrastructure.kv_transfer.connector.types.Request`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`
- ... and 1 more

---
*Auto-generated documentation*
