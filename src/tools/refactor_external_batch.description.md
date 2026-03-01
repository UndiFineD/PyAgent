# refactor_external_batch

**File**: `src\tools\refactor_external_batch.py`  
**Type**: Python Module  
**Summary**: 0 classes, 6 functions, 6 imports  
**Lines**: 178  
**Complexity**: 6 (moderate)

## Overview

Batch-safe refactor/copy of .external Python files into src/external_candidates.

Features:
- Recursively scans ROOT/.external for .py files
- Performs lightweight AST safety checks to detect `eval`, `exec`, `os.system`, `subprocess` usages
- Sanitizes filenames to snake_case and writes to a mirrored directory under `src/external_candidates/ingested`
- Produces a JSON mapping and log file, supports `--limit` and `--dry-run`

## Functions (6)

### `parse_allowlist(s)`

### `sanitize_filename(name)`

### `is_ast_safe(src, filename, allow_modules, allow_attrs, allow_names, allow_limited_shell, allow_eval)`

### `file_hash(p)`

### `process(limit, start, dry_run, verbose, allow_modules, allow_attrs, allow_names, allow_limited_shell, allow_eval)`

### `main()`

## Dependencies

**Imports** (6):
- `argparse`
- `ast`
- `hashlib`
- `json`
- `pathlib.Path`
- `re`

---
*Auto-generated documentation*
