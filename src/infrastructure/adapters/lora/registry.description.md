# registry

**File**: `src\infrastructure\adapters\lora\registry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 119  
**Complexity**: 8 (moderate)

## Overview

LRU registry for managing multiple LoRA models.

## Classes (2)

### `LoRAModelEntry`

Entry in the LoRA registry.

**Methods** (1):
- `touch(self)`

### `LoRARegistry`

Registry for managing multiple LoRA adapters.

**Methods** (7):
- `__init__(self, max_memory_bytes, max_models)`
- `register(self, model)`
- `get(self, model_id)`
- `unregister(self, model_id)`
- `_evict_lru(self)`
- `list_models(self)`
- `get_stats(self)`

## Dependencies

**Imports** (6):
- `collections.OrderedDict`
- `config.LoRAModelState`
- `dataclasses.dataclass`
- `model.LoRAModel`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
