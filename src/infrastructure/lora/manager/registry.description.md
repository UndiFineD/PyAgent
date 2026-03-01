# registry

**File**: `src\infrastructure\lora\manager\registry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 49  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for registry.

## Classes (1)

### `LoRARegistry`

Registry for LoRA adapters with caching.

**Methods** (6):
- `__init__(self, max_cached)`
- `register(self, config)`
- `get(self, adapter_name)`
- `unregister(self, adapter_name)`
- `list_adapters(self)`
- `get_stats(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `adapter.LoRAAdapter`
- `collections.OrderedDict`
- `config.LoRAConfig`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
