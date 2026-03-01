# manager

**File**: `src\infrastructure\backend\vllm_advanced\lora\manager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 232  
**Complexity**: 15 (moderate)

## Overview

LoRA adapter manager.

## Classes (1)

### `LoraManager`

Manager for dynamic LoRA adapter switching.

**Methods** (15):
- `__init__(self, config, registry)`
- `is_available(self)`
- `register_adapter(self, name, path)`
- `unregister_adapter(self, name)`
- `get_adapter(self, name)`
- `activate(self, name)`
- `deactivate(self, name)`
- `_update_lru(self, name)`
- `_evict_lru(self)`
- `get_lora_request(self, name)`
- ... and 5 more methods

## Dependencies

**Imports** (12):
- `logging`
- `models.AdapterState`
- `models.HAS_LORA`
- `models.LoraAdapter`
- `models.LoraConfig`
- `registry.LoraRegistry`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
