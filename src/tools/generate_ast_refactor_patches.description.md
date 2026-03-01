# generate_ast_refactor_patches

**File**: `src\tools\generate_ast_refactor_patches.py`  
**Type**: Python Module  
**Summary**: 1 classes, 4 functions, 7 imports  
**Lines**: 128  
**Complexity**: 5 (moderate)

## Overview

Generate conservative AST-based refactor patch proposals for top-priority files.

This script:
- Loads the bandit report (.external/static_checks/bandit.json) or uses the prepared
  bandit_report.md to find top files by score.
- For each top file present under `src/external_candidates/auto/`, it transforms
  function-level calls to dangerous subprocess APIs into calls to a
  `safe_subprocess_run(...)` wrapper and inserts a conservative wrapper stub.
- Writes unified-diff patch files to `.external/patches_ast/` for human review.

Notes:
- This only writes patch proposals and does not modify source files.

## Classes (1)

### `SubprocessTransformer`

**Inherits from**: NodeTransformer

Class SubprocessTransformer implementation.

**Methods** (1):
- `visit_Call(self, node)`

## Functions (4)

### `load_bandit_results()`

### `top_files_from_bandit(results, top_n)`

### `create_patch_for_file(path)`

### `main()`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `difflib`
- `json`
- `pathlib.Path`
- `re`
- `sys`

---
*Auto-generated documentation*
