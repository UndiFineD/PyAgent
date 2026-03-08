# external_refactor_scan

**File**: `src\tools\external_refactor_scan.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 7 imports  
**Lines**: 175  
**Complexity**: 6 (moderate)

## Overview

Safe scanner for `.external` repository snapshots.
- Reads `.external/tracking.md` and extracts completed/integrated table rows.
- Builds a per-directory candidate list of files and exported functions/classes.
- Does NOT execute any external code; it only reads and regex-parses files.
- Produces `.external/refactor_report.md` and `.external/refactor_report.json`.

Usage (PowerShell):
python -m src.tools.external_refactor_scan

Run only after reviewing and ensuring safety.

## Functions (6)

### `extract_completed_from_tracking(tracking_path)`

### `scan_directory_for_candidates(dirpath)`

### `is_definition_in_src(name, src_root)`

### `build_reuse_report(external_root, src_root)`

### `write_reports(report, md_path, json_path)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `json`
- `os`
- `pathlib.Path`
- `re`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
