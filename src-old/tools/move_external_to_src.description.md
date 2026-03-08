# move_external_to_src

**File**: `src\tools\move_external_to_src.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 6 imports  
**Lines**: 55  
**Complexity**: 0 (simple)

## Overview

Move files from top-level external_candidates into src/external_candidates.
Tries `git mv` for tracked files, falls back to shutil.move for others.
Preserves directory structure and removes empty source dirs afterwards.

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `os`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
