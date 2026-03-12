
"""
LLM_CONTEXT_START

## Source: src-old/tools/fix_version_bottom.description.md

# fix_version_bottom

**File**: `src\tools\fix_version_bottom.py`  
**Type**: Python Module  
**Summary**: 0 classes, 1 functions, 1 imports  
**Lines**: 46  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for fix_version_bottom.

## Functions (1)

### `fix_file(path)`

## Dependencies

**Imports** (1):
- `os`

---
*Auto-generated documentation*
## Source: src-old/tools/fix_version_bottom.improvements.md

# Improvements for fix_version_bottom

**File**: `src\tools\fix_version_bottom.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 46 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fix_version_bottom_test.py` with pytest tests

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

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    version_lines = []
    others = []
    for line in lines:
        if 'from src.core.base.version import VERSION' in line or '__version__ = VERSION' in line:
            version_lines.append(line)
        else:
            others.append(line)
    
    if len(version_lines) == 2:
        # Find insertion point
        insert_pos = 0
        for i, line in enumerate(others):
            if line.startswith('import ') or line.startswith('from '):
                insert_pos = i
                break
        
        # If no imports found, insert after docstring or future
        if insert_pos == 0:
            for i, line in enumerate(others):
                if line.startswith('from __future__'):
                    insert_pos = i + 1
                    break
        
        final_lines = others[:insert_pos] + version_lines + others[insert_pos:]
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        return True
    return False

# Files identified from ruff output
files_to_fix = [
    'src/infrastructure/backend/LLMClient.py',
    'src/infrastructure/fleet/AgentEconomy.py',
    'src/infrastructure/fleet/AgentStore.py',
]


def main():
    """Run fixes as a script. Tests should import this module without side-effects."""
    for f in files_to_fix:
        try:
            if fix_file(f):
                print(f"Fixed {f}")
        except FileNotFoundError:
            # When running under tests or in partial checkouts some files may be absent;
            # avoid raising on import or during test collection.
            continue


if __name__ == "__main__":
    main()
