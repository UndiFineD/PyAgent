# config

**File**: `src\infrastructure\adapters\lora\config.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 3 imports  
**Lines**: 61  
**Complexity**: 3 (simple)

## Overview

Configuration for LoRA adapters.

## Classes (3)

### `LoRATarget`

**Inherits from**: Enum

Common LoRA target modules.

### `LoRAConfig`

Configuration for LoRA adapter.

**Methods** (3):
- `__post_init__(self)`
- `_validate(self)`
- `scaling(self)`

### `LoRAModelState`

**Inherits from**: Enum

State of a LoRA model in the manager.

## Dependencies

**Imports** (3):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`

---
*Auto-generated documentation*
