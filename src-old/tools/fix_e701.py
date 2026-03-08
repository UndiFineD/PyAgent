"""
LLM_CONTEXT_START

## Source: src-old/tools/fix_e701.description.md

# fix_e701

**File**: `src\tools\fix_e701.py`  
**Type**: Python Module  
**Summary**: 0 classes, 2 functions, 2 imports  
**Lines**: 71  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for fix_e701.

## Functions (2)

### `fix_e701_in_file(file_path)`

### `main()`

## Dependencies

**Imports** (2):
- `os`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_e701.improvements.md

# Improvements for fix_e701

**File**: `src\tools\fix_e701.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 71 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_e701_test.py` with pytest tests

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

import os
import re


def fix_e701_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    changed = False

    # regex for simple cases: if/elif/else/for/while/with/def/class followed by : then more text
    # e.g. "if cond: return val"
    # we want to exclude things like dicts or type hints
    # pattern: ^(indent)(keyword)(.*): (statement)$

    # We use a simpler approach: line by line, find colon followed by non-comment text on the same line
    # for specific keywords.

    keywords = [
        "if",
        "elif",
        "else",
        "for",
        "while",
        "with",
        "def",
        "try",
        "except",
        "finally",
    ]
    kw_pattern = re.compile(r"^(\s*)(" + "|".join(keywords) + r")\b(.*?):\s*(.+)$")

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue

        match = kw_pattern.match(line)
        if match:
            indent = match.group(1)
            kw = match.group(2)
            rest_of_header = match.group(3)
            # check if the rest of line is just a comment
            statement = match.group(4).strip()
            if statement.startswith("#"):
                new_lines.append(line)
                continue

            # Additional check: avoid splitting if it's a one-liner def that might be intentional or has semicolon
            # but E701 specifically flags colon one-liners.

            # Construct new lines
            new_lines.append(f"{indent}{kw}{rest_of_header}:\n")
            # statement might have its own comment
            new_lines.append(f"{indent}    {statement}\n")
            changed = True
        else:
            new_lines.append(line)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    return changed


def main():
    root_dir = "src"
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    if fix_e701_in_file(path):
                        print(f"Fixed E701 in {path}")
                        count += 1
                except Exception as e:
                    print(f"Error in {path}: {e}")
    print(f"Total files fixed: {count}")


if __name__ == "__main__":
    main()
