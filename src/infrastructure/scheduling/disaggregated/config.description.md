# config

**File**: `src\infrastructure\scheduling\disaggregated\config.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 9 imports  
**Lines**: 166  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for config.

## Classes (4)

### `InstanceInfo`

Information about a vLLM instance.

Inspired by vLLM's proxy server patterns.

**Methods** (3):
- `base_url(self)`
- `kv_address(self)`
- `load_score(self)`

### `DCPConfig`

Configuration for disaggregated prefill-decode.

Inspired by vLLM's kv_transfer configuration.

### `KVTransferParams`

Parameters for KV cache transfer between instances.

Inspired by vLLM's kv_transfer_params dict structure.

**Methods** (2):
- `to_dict(self)`
- `from_dict(cls, data)`

### `ScheduledRequest`

A request scheduled for processing.

## Dependencies

**Imports** (9):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.InstanceRole`
- `enums.SchedulingPolicy`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
