# engine

**File**: `src\infrastructure\lora\manager\engine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 49  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for engine.

## Classes (1)

### `LoRAManager`

High-level LoRA management.

**Methods** (9):
- `__init__(self, max_loras, max_gpu_slots, max_rank)`
- `load_adapter(self, config)`
- `unload_adapter(self, name)`
- `add_request(self, request)`
- `remove_request(self, rid)`
- `get_adapter(self, name)`
- `list_loaded_adapters(self)`
- `get_active_adapters(self)`
- `get_stats(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `adapter.LoRAAdapter`
- `config.LoRAConfig`
- `config.LoRAInfo`
- `config.LoRARequest`
- `registry.LoRARegistry`
- `slot.LoRASlotManager`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
