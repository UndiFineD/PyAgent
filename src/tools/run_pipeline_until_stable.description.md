# run_pipeline_until_stable

**File**: `src\tools\run_pipeline_until_stable.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 5 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `pathlib.Path`
- `subprocess`
- `sys`
- `time`

---
*Auto-generated documentation*
