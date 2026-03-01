# batch_extract

**File**: `src\tools\batch_extract.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 10 imports  
**Lines**: 111  
**Complexity**: 4 (simple)

## Overview

Batch extractor: split a large refactor report into chunks and run
`extract_candidates.py` in parallel subprocesses.

This script creates temporary chunked reports under `.external/tmp_reports/`
and invokes the extractor on each chunk. It forwards relaxed flags so you can
extract broadly. Use `--allow-top-level` and `--allow-no-defs` to be permissive.

WARNING: this automates extraction at scale and may produce many files. Do not
run on untrusted machines unless you understand the risks.

## Functions (4)

### `chunk_files(report, chunk_size)`

### `make_chunk_report(chunk, idx)`

### `run_chunk(report_path, args_extra)`

### `main()`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `argparse`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.as_completed`
- `json`
- `math`
- `pathlib.Path`
- `shutil`
- `subprocess`
- `tempfile`

---
*Auto-generated documentation*
