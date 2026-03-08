# run_auto_tests

**File**: `src\tools\run_auto_tests.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 7 imports  
**Lines**: 64  
**Complexity**: 2 (simple)

## Overview

Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.

## Functions (2)

### `_run_file(path_str)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `argparse`
- `concurrent.futures`
- `os`
- `pathlib.Path`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
