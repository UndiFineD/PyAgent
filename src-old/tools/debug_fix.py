"""
LLM_CONTEXT_START

## Source: src-old/tools/debug_fix.description.md

# debug_fix

**File**: `src\tools\debug_fix.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 4 imports  
**Lines**: 80  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for debug_fix.

## Functions (1)

### `debug_fix(path)`

## Dependencies

**Imports** (4):
- `ast`
- `os`
- `re`
- `traceback`

---
*Auto-generated documentation*
## Source: src-old/tools/debug_fix.improvements.md

# Improvements for debug_fix

**File**: `src\tools\debug_fix.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `debug_fix_test.py` with pytest tests

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

import ast
import os
import re


def debug_fix(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    tree = ast.parse(content)
    lines = content.splitlines()
    import_nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]

    import_line_indices = set()
    for node in import_nodes:
        for i in range(node.lineno - 1, node.end_lineno):
            import_line_indices.add(i)

    extracted_imports = []
    seen_imports = set()
    for i in sorted(list(import_line_indices)):
        line = lines[i]
        if line.strip() not in seen_imports:
            extracted_imports.append(line)
            seen_imports.add(line.strip())

    other_lines = [lines[i] for i in range(len(lines)) if i not in import_line_indices]

    final_output = []
    if other_lines and other_lines[0].startswith("#!"):
        final_output.append(other_lines.pop(0))

    first_block_comments = []
    while other_lines and (
        other_lines[0].strip().startswith("#") or not other_lines[0].strip()
    ):
        line = other_lines.pop(0)
        if line.strip() == "":
            continue
        first_block_comments.append(line)

    final_output.extend(first_block_comments)
    final_output.append("")

    if other_lines and (
        other_lines[0].strip().startswith('"""')
        or other_lines[0].strip().startswith("'''")
    ):
        while other_lines:
            l = other_lines.pop(0)
            final_output.append(l)
            if '"""' in l or "'''" in l:
                if l.count('"""') == 2 or l.count("'''") == 2:
                    break
                while other_lines:
                    l2 = other_lines.pop(0)
                    final_output.append(l2)
                    if '"""' in l2 or "'''" in l2:
                        break
                break
        final_output.append("")

    future_imports = [i for i in extracted_imports if "__future__" in i]
    other_imports = [i for i in extracted_imports if "__future__" not in i]

    final_output.extend(future_imports)
    final_output.extend(other_imports)
    final_output.append("")

    for line in other_lines:
        final_output.append(line)

    res = "\n".join(final_output)
    print("--- FIRST 100 LINES OF RESULT ---")
    print("\n".join(res.splitlines()[:100]))

    try:
        ast.parse(res)
    except Exception as e:
        print(f"FAILED: {e}")
        # Find the line with the error
        import traceback

        lines_res = res.splitlines()
        if hasattr(e, "lineno"):
            print(f"Error at line {e.lineno}: {lines_res[e.lineno-1]}")


debug_fix("src/core/base/BaseAgent.py")
