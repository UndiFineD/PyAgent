# manager

**File**: `src\infrastructure\metrics\lora\manager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 276  
**Complexity**: 20 (complex)

## Overview

LoRA Stats Manager - Collection of aggregate stats for LoRA adapters.

## Classes (1)

### `LoRAStatsManager`

Manager for LoRA statistics collection.

Features:
- Thread-safe statistics updates
- Per-adapter tracking
- Request lifecycle tracking
- Memory tracking

**Methods** (20):
- `__init__(self, max_loaded_adapters)`
- `register_adapter(self, adapter_id, rank, alpha, target_modules, memory_bytes)`
- `start_loading(self, adapter_id)`
- `finish_loading(self, adapter_id, success)`
- `start_evicting(self, adapter_id)`
- `finish_evicting(self, adapter_id)`
- `create_request(self, request_id, adapter_id)`
- `start_request_loading(self, request_id)`
- `finish_request_loading(self, request_id)`
- `start_execution(self, request_id)`
- ... and 10 more methods

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `logging`
- `src.infrastructure.metrics.lora.types.LoRAAdapterInfo`
- `src.infrastructure.metrics.lora.types.LoRALoadState`
- `src.infrastructure.metrics.lora.types.LoRARequestState`
- `src.infrastructure.metrics.lora.types.LoRAStats`
- `threading`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
