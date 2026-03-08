"""
LLM_CONTEXT_START

## Source: src-old/tools/fix_e701_v2.description.md

# fix_e701_v2

**File**: `src\tools\fix_e701_v2.py`  
**Type**: Python Module  
**Summary**: 0 classes, 3 functions, 3 imports  
**Lines**: 94  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for fix_e701_v2.

## Functions (3)

### `is_balanced(s)`

Check if parentheses, brackets, and braces are balanced in a string.

### `fix_e701_in_file(file_path)`

### `main()`

## Dependencies

**Imports** (3):
- `ast`
- `os`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_e701_v2.improvements.md

# Improvements for fix_e701_v2

**File**: `src\tools\fix_e701_v2.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 94 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_e701_v2_test.py` with pytest tests

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
import ast

KEYWORDS = [
    "if",
    "elif",
    "else",
    "for",
    "while",
    "try",
    "except",
    "finally",
    "with",
    "def",
    "class",
]


def is_balanced(s):
    """Check if parentheses, brackets, and braces are balanced in a string."""
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    in_string = None
    escaped = False

    for i, char in enumerate(s):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if in_string:
            if char == in_string:
                in_string = None
            continue
        if char in ['"', "'"]:
            in_string = char
            continue
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
    return not stack and not in_string


def fix_e701_in_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    new_lines = []
    modified = False

    # Regex to catch kw ... : statement
    kw_pattern = re.compile(r"^(\s*)(" + "|".join(KEYWORDS) + r")\b(.*?):\s*(.+)$")

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue

        match = kw_pattern.match(line.rstrip())
        if match:
            indent, kw, header_rest, statement = match.groups()
            whole_header = f"{kw}{header_rest}"

            if is_balanced(whole_header) and not statement.strip().startswith(
                ('"', "'")
            ):
                # Double check that we aren't splitting a one-liner that is actually allowed (like def/class headers if they are empty, but here they have statements)
                # Ensure the statement doesn't look like part of a multi-line string start
                new_lines.append(f"{indent}{kw}{header_rest}:\n")
                new_lines.append(f"{indent}    {statement}\n")
                modified = True
                continue

        new_lines.append(line)

    if modified:
        try:
            content = "".join(new_lines)
            ast.parse(content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception:
            pass
    return False


def main():
    src_dir = r"C:\DEV\PyAgent\src"
    count = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                if fix_e701_in_file(path):
                    count += 1
                    print(f"Fixed E701 in {path}")
    print(f"Total files fixed: {count}")


if __name__ == "__main__":
    main()
