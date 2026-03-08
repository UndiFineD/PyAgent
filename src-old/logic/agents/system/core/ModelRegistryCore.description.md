# ModelRegistryCore

**File**: `src\logic\agents\system\core\ModelRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 68  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for ModelRegistryCore.

## Classes (1)

### `ModelRegistryCore`

ModelRegistryCore manages the PEFT (LoRA/QLoRA) adapter registry.
It maps request types to specific expert adapters.
Phase 289: Model Registry Self-Healing.

**Methods** (6):
- `__init__(self)`
- `self_heal(self)`
- `get_adapter_for_task(self, task_type)`
- `should_trigger_finetuning(self, quality_history, threshold)`
- `register_new_adapter(self, name, path)`
- `list_adapters(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
