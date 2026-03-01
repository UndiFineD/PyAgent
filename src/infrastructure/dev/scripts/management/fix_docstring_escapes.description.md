# fix_docstring_escapes

**File**: `src\infrastructure\dev\scripts\management\fix_docstring_escapes.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 56  
**Complexity**: 1 (simple)

## Overview

Utility to fix incorrectly escaped quotes in docstrings (common after bulk refactoring).
Ported from temp/fix_escaped_quotes.py.

## Functions (1)

### `fix_escapes(target_dirs)`

Recursively fixes """ and " in Python files.

## Dependencies

**Imports** (3):
- `argparse`
- `os`
- `pathlib.Path`

---
*Auto-generated documentation*
