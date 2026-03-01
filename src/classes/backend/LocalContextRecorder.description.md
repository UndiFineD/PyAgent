# LocalContextRecorder

**File**: `src\classes\backend\LocalContextRecorder.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 137  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for LocalContextRecorder.

## Classes (1)

### `LocalContextRecorder`

**Inherits from**: ContextRecorderInterface

Records LLM prompts and results for future training/fine-tuning.
Stores data in JSONL format with monthly and hash-based sharding.
Optimized for trillion-parameter data harvesting (Phase 105).

**Methods** (4):
- `__init__(self, workspace_root, user_context, fleet)`
- `record_interaction(self, provider, model, prompt, result, meta)`
- `record_lesson(self, tag, data)`
- `_update_index(self, prompt_hash, filename)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `datetime.datetime`
- `gzip`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseInterfaces.ContextRecorderInterface`
- `src.core.base.Version.VERSION`
- `src.core.rust_bridge.RustBridge`
- `typing.Any`
- `zlib`

---
*Auto-generated documentation*
