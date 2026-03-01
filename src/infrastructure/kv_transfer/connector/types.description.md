# types

**File**: `src\infrastructure\kv_transfer\connector\types.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 13 imports  
**Lines**: 104  
**Complexity**: 9 (moderate)

## Overview

Phase 45: KV Transfer Connector Types
Shared types and configurations for KV transfer connectors.

## Classes (7)

### `KVConnectorRole`

**Inherits from**: Enum

Role of the KV connector in disaggregated inference.

### `KVTransferMode`

**Inherits from**: Enum

Transfer mode for KV cache data.

### `KVTransferConfig`

Configuration for KV transfer operations.

**Methods** (3):
- `get_from_extra_config(self, key, default)`
- `is_producer(self)`
- `is_consumer(self)`

### `KVConnectorMetadata`

Metadata for KV transfer operations.

### `KVCacheBlocks`

Represents allocated KV cache blocks for a request.

**Methods** (3):
- `get_block_ids(self)`
- `get_unhashed_block_ids(self)`
- `total_tokens(self)`

### `ForwardContext`

**Inherits from**: Protocol

Protocol for forward context during model execution.

**Methods** (1):
- `attn_metadata(self)`

### `Request`

**Inherits from**: Protocol

Protocol for request objects.

**Methods** (2):
- `request_id(self)`
- `kv_transfer_params(self)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.Tuple`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
