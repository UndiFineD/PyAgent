# apply_patch_proposals

**File**: `src\tools\apply_patch_proposals.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 7 imports  
**Lines**: 108  
**Complexity**: 1 (simple)

## Overview

Apply conservative patch proposals generated from bandit findings.

This script re-uses the heuristics in `prepare_refactor_patches.py` to
produce safe, text-based replacements for flagged lines (e.g. comment out
risky imports, replace eval/exec with a RuntimeError), writes a backup
`*.bak` and updates the target file in-place.

This is intentionally conservative and deterministic so it can run
automatically in CI or overnight runs.

## Functions (1)

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `pathlib.Path`
- `shutil`
- `src.tools.prepare_refactor_patches`
- `sys`
- `tools.prepare_refactor_patches`

---
*Auto-generated documentation*
