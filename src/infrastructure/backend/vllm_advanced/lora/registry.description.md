# registry

**File**: `src\infrastructure\backend\vllm_advanced\lora\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 107  
**Complexity**: 8 (moderate)

## Overview

LoRA adapter registry.

## Classes (1)

### `LoraRegistry`

Registry for tracking available LoRA adapters.

Maintains a catalog of adapters that can be loaded on demand.

**Methods** (8):
- `__init__(self)`
- `register(self, name, path, base_model, rank, alpha, target_modules)`
- `unregister(self, name)`
- `get(self, name)`
- `get_by_id(self, adapter_id)`
- `list_adapters(self)`
- `list_loaded(self)`
- `find_by_base_model(self, base_model)`

## Dependencies

**Imports** (6):
- `logging`
- `models.AdapterState`
- `models.LoraAdapter`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
