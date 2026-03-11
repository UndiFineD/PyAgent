"""LLM_CONTEXT_START

## Source: src-old/tools/fix_e402_versions_v3.description.md

# fix_e402_versions_v3

**File**: `src\tools\fix_e402_versions_v3.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 3 imports  
**Lines**: 82  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for fix_e402_versions_v3.

## Functions (3)

### `is_syntax_valid(content)`

### `surgical_fix_e402(file_path)`

### `main()`

## Dependencies

**Imports** (3):
- `ast`
- `os`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_e402_versions_v3.improvements.md

# Improvements for fix_e402_versions_v3

**File**: `src\tools\fix_e402_versions_v3.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 82 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_e402_versions_v3_test.py` with pytest tests

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


def is_syntax_valid(content):
    try:
        ast.parse(content)
        return True
    except SyntaxError:
        return False


def surgical_fix_e402(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    if "__version__ = VERSION" not in content:
        return False

    lines = content.splitlines(keepends=True)
    last_top_level_import_idx = -1
    version_assignment_idx = -1

    for i, line in enumerate(lines):
        # Only consider top-level assignments
        if line.startswith("__version__ = VERSION"):
            version_assignment_idx = i
        # Only consider top-level imports
        if line.startswith(("import ", "from ")):
            last_top_level_import_idx = i

    if (
        version_assignment_idx != -1
        and last_top_level_import_idx > version_assignment_idx
    ):
        # We need to move the assignment after the last top-level import.
        # But wait, we should also check if there are any imports after the assignment.
        # If there are NO imports after the assignment at the top level, then E402 shouldn't be triggered by this.
        # However, Ruff might be complaining if there are indented imports later?
        # Actually E402 is specifically about module-level imports.

        assignment_line = lines.pop(version_assignment_idx)

        # Re-find last top-level import index after pop
        last_top_level_import_idx = -1
        for i, line in enumerate(lines):
            if line.startswith(("import ", "from ")):
                last_top_level_import_idx = i

        # Insert after the last top-level import
        lines.insert(last_top_level_import_idx + 1, assignment_line)

        new_content = "".join(lines)

        if is_syntax_valid(new_content):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        else:
            print(f"Skipping {file_path} - would introduce syntax error")
            return False

    return False


def main():
    src_dir = r"C:\DEV\PyAgent\src"
    count = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    if surgical_fix_e402(path):
                        count += 1
                        print(f"Fixed E402 (VERSION) in {path}")
                except Exception as e:
                    print(f"Failed to process {path}: {e}")

    print(f"Total files fixed: {count}")


if __name__ == "__main__":
    main()
