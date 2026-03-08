"""
LLM_CONTEXT_START

## Source: src-old/tools/find_syntax_errors.description.md

# find_syntax_errors

**File**: `src\tools\find_syntax_errors.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 2 imports  
**Lines**: 19  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for find_syntax_errors.

## Functions (1)

### `find_syntax_errors(root_dir)`

## Dependencies

**Imports** (2):
- `ast`
- `os`

---
*Auto-generated documentation*
## Source: src-old/tools/find_syntax_errors.improvements.md

# Improvements for find_syntax_errors

**File**: `src\tools\find_syntax_errors.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 19 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `find_syntax_errors_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import ast
import os


def find_syntax_errors(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        ast.parse(f.read())
                except SyntaxError as e:
                    print(f"Syntax Error in {path}: {e}")
                except Exception as e:
                    # Some files might have encoding issues
                    pass


if __name__ == "__main__":
    find_syntax_errors("src")
