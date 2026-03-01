# models

**File**: `src\infrastructure\backend\vllm_advanced\lora\models.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 12 imports  
**Lines**: 108  
**Complexity**: 3 (simple)

## Overview

Models and configuration for LoRA adapters.

## Classes (3)

### `AdapterState`

**Inherits from**: Enum

State of a LoRA adapter.

### `LoraConfig`

Configuration for LoRA loading and management.

### `LoraAdapter`

Represents a LoRA adapter.

**Methods** (3):
- `hash(self)`
- `to_lora_request(self)`
- `mark_used(self)`

## Dependencies

**Imports** (12):
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `hashlib`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `vllm.lora.request.LoRARequest`

---
*Auto-generated documentation*
