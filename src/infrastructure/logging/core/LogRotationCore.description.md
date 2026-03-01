# LogRotationCore

**File**: `src\infrastructure\logging\core\LogRotationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 65  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for LogRotationCore.

## Classes (1)

### `LogRotationCore`

LogRotationCore handles rolling log file strategies with compression.
It isolates the logic from the logging framework itself for future Rust migration.

**Methods** (4):
- `__init__(self, log_dir, max_size_bytes)`
- `should_rotate(self, file_path)`
- `rotate_and_compress(self, file_path)`
- `calculate_log_level(self, fleet_health_score)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `datetime.datetime`
- `gzip`
- `os`
- `shutil`
- `typing.Optional`

---
*Auto-generated documentation*
