"""LLM_CONTEXT_START

## Source: src-old/tools/fix_f401_inits_v2.description.md

# fix_f401_inits_v2

**File**: `src\tools\fix_f401_inits_v2.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 2 imports  
**Lines**: 58  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for fix_f401_inits_v2.

## Functions (1)

### `fix_init_file(filepath)`

## Dependencies

**Imports** (2):
- `ast`
- `os`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_f401_inits_v2.improvements.md

# Improvements for fix_f401_inits_v2

**File**: `src\tools\fix_f401_inits_v2.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 58 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_f401_inits_v2_test.py` with pytest tests

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


def fix_init_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    new_lines = []
    modified = False
    for line in lines:
        stripped = line.strip()
        # Look for: from .Something import Name
        # Must be single import, no alias, no star, no multiple names
        if (
            (stripped.startswith("from .") or stripped.startswith("from src."))
            and " import " in stripped
            and " as " not in stripped
            and "," not in stripped
            and "*" not in stripped
        ):
            parts = stripped.split(" import ")
            if len(parts) == 2:
                module_part = parts[0]
                name = parts[1].strip()
                if " " not in name and name.isidentifier():  # Single valid identifier
                    indent = line[: line.find("from")]
                    # Preserve trailing comments if any
                    comment = ""
                    if "#" in name:
                        # This shouldn't happen with stripped and no space, but let's be safe
                        pass

                    # Ensure we don't double-alias if the name is already an alias in a complex line (though we checked ' as ')
                    new_line = f"{indent}{module_part} import {name} as {name}\n"
                    new_lines.append(new_line)
                    modified = True
                    continue
        new_lines.append(line)

    if modified:
        content = "".join(new_lines)
        try:
            ast.parse(content)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {filepath}")
            return True
        except Exception as e:
            print(f"Failed validation for {filepath}: {e}")
            return False
    return False


if __name__ == "__main__":
    count = 0
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file == "__init__.py":
                if fix_init_file(os.path.join(root, file)):
                    count += 1
    print(f"Total __init__.py files fixed: {count}")
