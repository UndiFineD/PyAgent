# LocalContextRecorder

**File**: `src\infrastructure\compute\backend\LocalContextRecorder.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 78  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for LocalContextRecorder.

## Classes (1)

### `LocalContextRecorder`

Records LLM prompts and results for future training/fine-tuning.
Stores data in JSONL format with monthly and hash-based sharding.
Optimized for trillion-parameter data harvesting (Phase 105).

**Methods** (3):
- `__init__(self, workspace_root)`
- `record_interaction(self, provider, model, prompt, result, meta)`
- `_update_index(self, prompt_hash, filename)`

## Dependencies

**Imports** (10):
- `datetime.datetime`
- `gzip`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `zlib`

---
*Auto-generated documentation*
