# adapter

**File**: `src\infrastructure\lora\manager\adapter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 2 functions, 16 imports  
**Lines**: 108  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for adapter.

## Classes (1)

### `LoRAAdapter`

Represents a loaded LoRA adapter.

**Methods** (10):
- `__init__(self, config)`
- `name(self)`
- `status(self)`
- `load(self)`
- `_load_from_dir(self, path)`
- `_load_st(self, path)`
- `_load_torch(self, path)`
- `_extract_module(self, key)`
- `apply_to_linear(self, module_name, hidden_states)`
- `merge_into_weights(self, original_weights)`

## Functions (2)

### `load_lora_adapter(path, name, rank, scale)`

### `get_lora_info(path)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `config.AdapterStatus`
- `config.LoRAConfig`
- `config.LoRAInfo`
- `config.LoRAMethod`
- `json`
- `numpy`
- `pathlib.Path`
- `safetensors.safe_open`
- `time`
- `torch`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
