# StructuredLogger

**File**: `src\observability\StructuredLogger.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 178  
**Complexity**: 10 (moderate)

## Overview

StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.

## Classes (1)

### `StructuredLogger`

JSON logger for PyAgent swarm observability.
Phase 277: Added log hygiene with automated GZIP compression.

**Methods** (10):
- `__init__(self, agent_id, trace_id, log_file)`
- `_ensure_log_dir(self)`
- `_compress_logs(self)`
- `_mask_sensitive(self, text)`
- `log(self, level, message)`
- `info(self, message)`
- `error(self, message)`
- `warning(self, message)`
- `debug(self, message)`
- `success(self, message)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `datetime.datetime`
- `datetime.timezone`
- `gzip`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `rust_core`
- `shutil`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
