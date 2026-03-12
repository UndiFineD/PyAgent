"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/KnowledgeTransferCore.description.md

# KnowledgeTransferCore

**File**: `src\\classes\fleet\\KnowledgeTransferCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 31  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for KnowledgeTransferCore.

## Classes (1)

### `KnowledgeTransferCore`

Pure logic for Knowledge Transfer.
Handles merging of lesson datasets.

**Methods** (1):
- `merge_lessons(self, current_lessons, imported_lessons)`

## Dependencies

**Imports** (4):
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/KnowledgeTransferCore.improvements.md

# Improvements for KnowledgeTransferCore

**File**: `src\\classes\fleet\\KnowledgeTransferCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 31 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeTransferCore_test.py` with pytest tests

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

from typing import Any, List, Set


class KnowledgeTransferCore:
    """Pure logic for Knowledge Transfer.
    Handles merging of lesson datasets.
    """

    def merge_lessons(
        self, current_lessons: List[Any], imported_lessons: List[Any]
    ) -> List[Any]:
        """Merges imported lessons into the current set, avoiding duplicates."""
        # Normalize to dicts only
        valid_current = [l for l in current_lessons if isinstance(l, dict)]
        valid_imported = [l for l in imported_lessons if isinstance(l, dict)]

        # Create a signature set for existing lessons
        # Signature = (failure_context, correction) usually unique enough
        seen_signatures: Set[str] = set()

        for l in valid_current:
            sig = f"{l.get('failure_context')}|{l.get('correction')}"
            seen_signatures.add(sig)

        merged = list(valid_current)  # Start with current

        for lesson in valid_imported:
            sig = f"{lesson.get('failure_context')}|{lesson.get('correction')}"
            if sig not in seen_signatures:
                merged.append(lesson)
                seen_signatures.add(sig)

        return merged
