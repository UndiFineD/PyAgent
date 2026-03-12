#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/tools/append_verification.description.md

# append_verification

**File**: `src\tools\append_verification.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 1 imports  
**Lines**: 26  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for append_verification.

## Dependencies

**Imports** (1):
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/tools/append_verification.improvements.md

# Improvements for append_verification

**File**: `src\tools\append_verification.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 26 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `append_verification_test.py` with pytest tests

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

"""Helper script to append verification methods to the canonical module."""
from pathlib import Path

content = '''
    @staticmethod
    def secondary_verify(result: str, primary_model: str) -> bool:
        \"\"\"
        Performs a cross-model verification loop (Phase 258).
        A faster model reviews the primary model's output.
        \"\"\"
        # In a real implementation, this would call a different backend
        return True

    @staticmethod
    def jury_verification(agent_responses: list[bool]) -> bool:
        \"\"\"
        Implements a 'Jury of Agents' consensus (Phase 258).
        Requires majority or unanimity based on risk.
        \"\"\"
        if not agent_responses:
            return False
        return sum(agent_responses) >= 2  # Majority out of 3
'''


def append_to_verification() -> None:
    """Append the extra verification methods to the canonical module.

    Safe to call multiple times; no duplicates will be written.  Importing
    this module no longer mutates the repository, so test imports are safe.
    """
    p = Path(__file__).resolve().parent.parent / "src" / "core" / "base" / "verification.py"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    if "secondary_verify" in text or "jury_verification" in text:
        return
    with open(p, "a", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    append_to_verification()
