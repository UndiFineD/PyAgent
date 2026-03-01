# slot

**File**: `src\infrastructure\lora\manager\slot.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 60  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for slot.

## Classes (1)

### `LoRASlotManager`

Manages GPU slots for LoRA adapters.

**Methods** (7):
- `__init__(self, num_slots)`
- `allocate(self, adapter_name, memory)`
- `_fill_slot(self, slot, name, mem)`
- `release(self, name)`
- `evict(self, name)`
- `get_active_adapters(self)`
- `get_stats(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `config.AdapterSlot`
- `threading`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
