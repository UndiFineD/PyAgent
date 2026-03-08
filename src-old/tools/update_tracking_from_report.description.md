# update_tracking_from_report

**File**: `src\tools\update_tracking_from_report.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 2 imports  
**Lines**: 116  
**Complexity**: 6 (moderate)

## Overview

Small utility: parse .external/refactor_report.json and update
.external/tracking.md and .external/completed.md, plus generate
.external/candidates.md with prioritized candidates.

This script is read-only for scanned files and only appends/edits
the tracking/completed/candidates files in-place. It does not
execute any code found in .external.

## Functions (6)

### `load_report()`

### `append_tracking(rows)`

### `move_completed_rows()`

### `build_candidates(report, limit)`

### `write_candidates(cands)`

### `main()`

## Dependencies

**Imports** (2):
- `json`
- `pathlib.Path`

---
*Auto-generated documentation*
