# run_full_pipeline

**File**: `src\tools\run_full_pipeline.py`  
**Type**: Python Module  
**Summary**: 0 classes, 8 functions, 20 imports  
**Lines**: 662  
**Complexity**: 8 (moderate)

## Overview

Orchestrate the full external->src pipeline end-to-end with no prompts.

Steps (non-interactive):
  1. Run `batch_extract.py` to extract candidates into `src/external_candidates/auto/`
  2. Run `run_static_checks.py` against the extracted candidates
  3. Run `run_auto_tests.py` to execute generated tests
  4. Run `move_completed.py` to move completed tracking rows (idempotent)
  5. Regenerate `docs/architecture/external_integration.md` summary

This script returns a non-zero exit code if critical steps fail.

## Functions (8)

### `run(cmd, fatal)`

### `compute_sha(path_str)`

Compute sha256 for a file path string (module-level worker).

### `run_checks_for_sha(args)`

Run bandit/semgrep/python-only checks for a single file and write per-sha outputs.
Args: (sha, path_str)
Returns: (sha, results dict)

### `summarize_and_write_doc()`

### `update_refactor_report(report_path, extracted_files)`

### `write_refactor_report_md(report_path, md_path)`

### `_is_init(p)`

### `main()`

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `ast`
- `concurrent.futures`
- `datetime.datetime`
- `hashlib`
- `json`
- `os`
- `pathlib.Path`
- `shutil`
- `sqlite3`
- `src.tools.apply_safe_fixes`
- `src.tools.prepare_refactor_patches`
- `src.tools.run_auto_tests`
- `src.tools.run_static_checks`
- `subprocess`
- ... and 5 more

---
*Auto-generated documentation*
