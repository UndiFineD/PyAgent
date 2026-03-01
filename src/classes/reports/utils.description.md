# utils

**File**: `src\classes\reports\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 8 functions, 7 imports  
**Lines**: 121  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for utils.

## Functions (8)

### `_read_text(path)`

Read text file with UTF-8 and replacement errors.

### `_is_pytest_test_file(path)`

Check if file is a pytest test file.

### `_looks_like_pytest_import_problem(path)`

Check if filename has characters that cause pytest import issues.

### `_find_imports(tree)`

Find all top-level imports in an AST.

### `_detect_argparse(source)`

Check if source uses argparse.

### `_placeholder_test_note(path, source)`

Check if it's a placeholder test file.

### `_rel(path)`

Get relative path string for display.

### `_find_issues(tree, source)`

Find potential issues via lightweight static analysis.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `pathlib.Path`
- `re`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
