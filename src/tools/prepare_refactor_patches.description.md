# prepare_refactor_patches

**File**: `src\tools\prepare_refactor_patches.py`  
**Type**: Python Module  
**Summary**: 0 classes, 7 functions, 6 imports  
**Lines**: 132  
**Complexity**: 7 (moderate)

## Overview

Generate prioritized bandit report and prepare AST-based refactor patch proposals.

Produces:
- .external/static_checks/bandit_report.md  (summary, prioritized)
- .external/patches/<sanitized_filename>.patch  (human-review patch proposals)

This script does NOT apply patches; it only writes suggestions for reviewers.

## Functions (7)

### `sanitize_name(p)`

### `load_bandit()`

### `aggregate(results)`

### `make_report(agg, top_n)`

### `create_patch_proposal(filename, findings)`

### `suggest_replacement(line)`

### `main()`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `ast`
- `json`
- `pathlib.Path`
- `re`
- `shutil`

---
*Auto-generated documentation*
