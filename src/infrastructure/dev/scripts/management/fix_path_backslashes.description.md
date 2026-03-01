# fix_path_backslashes

**File**: `src\infrastructure\dev\scripts\management\fix_path_backslashes.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 56  
**Complexity**: 1 (simple)

## Overview

Utility to fix backslash escaping issues in paths (e.g., c:" -> c:\").
Ported from temp/fix_backslashes.py.

## Functions (1)

### `fix_path_backslashes(target_dirs)`

Recursively fixes malformed path strings in Python files.

## Dependencies

**Imports** (3):
- `argparse`
- `os`
- `pathlib.Path`

---
*Auto-generated documentation*
