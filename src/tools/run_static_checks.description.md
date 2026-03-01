# run_static_checks

**File**: `src\tools\run_static_checks.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 7 imports  
**Lines**: 143  
**Complexity**: 3 (simple)

## Overview

Run static-safety checks on extracted candidates.
Tries to run `bandit` and `semgrep` if available. Writes JSON outputs under ./.external/static_checks/
Usage:
  python src/tools/run_static_checks.py src/external_candidates/auto

## Functions (3)

### `run_python_only_checks(target)`

Run fast AST-based checks for banned imports/names and dangerous calls.
Returns a mapping of file -> list of findings.

### `run_check(check, target)`

### `main(argv)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `json`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
