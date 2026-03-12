"""LLM_CONTEXT_START

## Source: src-old/tools/clean_sys_path.description.md

# clean_sys_path

**File**: `src\tools\\clean_sys_path.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 36  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for clean_sys_path.

## Functions (1)

### `remove_sys_path_hacks()`

## Dependencies

**Imports** (3):
- `os`
- `pathlib.Path`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/clean_sys_path.improvements.md

# Improvements for clean_sys_path

**File**: `src\tools\\clean_sys_path.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 36 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `clean_sys_path_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import os
import re
from pathlib import Path


def remove_sys_path_hacks():
    root_dir = Path("C:/DEV/PyAgent")
    tests_dir = root_dir / "tests"

    # Patterns to match:
    # sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))
    # sys.path.insert(0, str(AGENT_DIR))
    # etc.

    # We want to keep imports, but remove the sys.path manipulation.

    patterns = [
        re.compile(r"^\s*sys\.path\.insert\(.*?\)\s*$", re.MULTILINE),
        re.compile(r"^\s*sys\.path\.append\(.*?\)\s*$", re.MULTILINE),
    ]

    for root, dirs, files in os.walk(tests_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                content = file_path.read_text(encoding="utf-8")

                original_content = content
                for p in patterns:
                    content = p.sub("", content)

                if content != original_content:
                    print(f"Cleaning {file_path}")
                    file_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    remove_sys_path_hacks()
