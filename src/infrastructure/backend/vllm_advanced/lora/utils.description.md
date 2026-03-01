# utils

**File**: `src\infrastructure\backend\vllm_advanced\lora\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 10 imports  
**Lines**: 64  
**Complexity**: 2 (simple)

## Overview

Utilities for LoRA adapter management.

## Functions (2)

### `create_lora_request(name, adapter_id, path)`

Create a LoRARequest directly.

### `discover_adapters(directory, pattern)`

Discover LoRA adapters in a directory.

## Dependencies

**Imports** (10):
- `json`
- `logging`
- `models.HAS_LORA`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`
- `vllm.lora.request.LoRARequest`

---
*Auto-generated documentation*
