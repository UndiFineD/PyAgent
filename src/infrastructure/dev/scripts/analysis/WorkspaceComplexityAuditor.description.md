# WorkspaceComplexityAuditor

**File**: `src\infrastructure\dev\scripts\analysis\WorkspaceComplexityAuditor.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 5 imports  
**Lines**: 76  
**Complexity**: 1 (simple)

## Overview

Auditor for workspace code complexity using Rust-native analysis.
Ported from temp/find_complex_files.py for re-use in the fleet.

## Functions (1)

### `run_audit(target_dir, threshold, limit)`

Scans the target directory for Python files exceeding the complexity threshold.

## Dependencies

**Imports** (5):
- `argparse`
- `logging`
- `os`
- `pathlib.Path`
- `rust_core`

---
*Auto-generated documentation*
