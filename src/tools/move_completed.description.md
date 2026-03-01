# move_completed

**File**: `src\tools\move_completed.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 3 imports  
**Lines**: 94  
**Complexity**: 3 (simple)

## Overview

Move completed rows from .external/tracking.md to .external/completed.md

Idempotent: will not duplicate entries already present in completed.md.
It treats table rows where the second column (status) contains
case-insensitive 'completed'|'done'|'finished' as completed.

## Functions (3)

### `parse_row(line)`

### `is_completed_status(s)`

### `main()`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `datetime`
- `pathlib.Path`

---
*Auto-generated documentation*
