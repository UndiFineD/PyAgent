# IncrementalProcessor

**File**: `src\core\base\IncrementalProcessor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 231  
**Complexity**: 11 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `IncrementalProcessor`

Processes only files changed since last run.

Tracks file modification times and content hashes to enable
incremental processing, avoiding reprocessing unchanged files.
Phases 233/271: Uses BLAKE3 and CBOR with buffered reads for performance.

Attributes:
    state_file: Path to state persistence file.
    state: Current incremental processing state.

**Methods** (11):
- `__init__(self, repo_root, state_file)`
- `_load_state(self)`
- `_apply_state_data(self, data)`
- `_save_state(self)`
- `_compute_file_hash(self, file_path)`
- `validate_hashes(self, files)`
- `batch_requests(self, files, token_limit)`
- `get_changed_files(self, files)`
- `mark_processed(self, file_path)`
- `complete_run(self)`
- ... and 1 more methods

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `blake3`
- `cbor2`
- `logging`
- `mmap`
- `orjson`
- `os`
- `pathlib.Path`
- `src.core.base.models.IncrementalState`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
