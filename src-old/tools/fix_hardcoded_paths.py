"""
LLM_CONTEXT_START

## Source: src-old/tools/fix_hardcoded_paths.description.md

# fix_hardcoded_paths

**File**: `src\tools\fix_hardcoded_paths.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 3 imports  
**Lines**: 60  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for fix_hardcoded_paths.

## Functions (1)

### `fix_hardcoded_paths()`

## Dependencies

**Imports** (3):
- `os`
- `pathlib.Path`
- `re`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_hardcoded_paths.improvements.md

# Improvements for fix_hardcoded_paths

**File**: `src\tools\fix_hardcoded_paths.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 60 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_hardcoded_paths_test.py` with pytest tests

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
from pathlib import Path


def fix_hardcoded_paths():
    root_dir = Path("C:/DEV/PyAgent")

    # regex for c:/DEV/PyAgent or C:/DEV/PyAgent or c:\\DEV\\PyAgent
    pattern = re.compile(r"c:/DEV/PyAgent", re.IGNORECASE)

    # Scan src and tests
    for target_dir in [root_dir / "src", root_dir / "tests"]:
        if not target_dir.exists():
            continue
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    content = file_path.read_text(encoding="utf-8")

                    if pattern.search(content):
                        print(f"Fixing {file_path}")
                        # Determine parents count based on depth from root
                        rel_path = file_path.relative_to(root_dir)
                        parents_count = len(rel_path.parents) - 1

                        prefix = f"Path(__file__).resolve().parents[{parents_count}]"

                        # Replace full paths or partial paths starting with root
                        def replacer(match):
                            # We want to replace "C:/DEV/PyAgent/..." with Path(...) / "..."
                            # But wait, we need to handle quotes.
                            return f"{{ROOT_PLACEHOLDER}}"

                        # Simpler: replace the string root with {ROOT} and then fix it up
                        content = content.replace("c:/DEV/PyAgent", "C:/DEV/PyAgent")
                        content = content.replace("C:/DEV/PyAgent", "{ROOT}")

                        # Fix up: "Path(__file__).resolve().parents[N] / 'src'"
                        # But wait, if it was in a string: "C:/DEV/PyAgent/src" -> "{ROOT}/src"
                        # We need to change the string to a Path object or similar.

                        # Search for "{ROOT}/..." inside strings
                        # e.g. "Path('{ROOT}/src')" or just "{ROOT}/src"

                        # Let's try something simpler:
                        # Replace '"C:/DEV/PyAgent' with 'str(Path(__file__).resolve().parents[N])' + '
                        content = content.replace('"{ROOT}', f'str({prefix}) + "')
                        content = content.replace("'{ROOT}", f"str({prefix}) + '")

                        # And handle cases where it's the exact string
                        content = content.replace(f'"{prefix}"', prefix)
                        content = content.replace(f"'{prefix}'", prefix)

                        # Handle leftover {ROOT} if any
                        content = content.replace("{ROOT}", f"str({prefix})")

                        file_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    fix_hardcoded_paths()
