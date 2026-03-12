"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/core/LessonCore.description.md

# LessonCore

**File**: `src\logic\agents\swarm\core\LessonCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 42  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for LessonCore.

## Classes (2)

### `Lesson`

Class Lesson implementation.

### `LessonCore`

Pure logic for cross-fleet lesson aggregation.
Uses bloom-filter-like hashing to track known failure modes.

**Methods** (5):
- `__init__(self)`
- `generate_failure_hash(self, error_msg)`
- `is_known_failure(self, error_msg)`
- `record_lesson(self, lesson)`
- `get_related_lessons(self, error_msg, all_lessons)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `hashlib`
- `typing.List`
- `typing.Set`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/core/LessonCore.improvements.md

# Improvements for LessonCore

**File**: `src\logic\agents\swarm\core\LessonCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 42 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: Lesson

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LessonCore_test.py` with pytest tests

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

from __future__ import annotations

import hashlib
from typing import List, Set
from dataclasses import dataclass


@dataclass
class Lesson:
    error_pattern: str
    cause: str
    solution: str
    impact_score: float = 0.5


class LessonCore:
    """Pure logic for cross-fleet lesson aggregation.
    Uses bloom-filter-like hashing to track known failure modes.
    """

    def __init__(self) -> None:
        self.known_failures: set[str] = set()

    def generate_failure_hash(self, error_msg: str) -> str:
        """Generates a stable hash for an error message (ignoring line numbers/paths)."""
        # Simple normalization: lower case and strip numbers
        normalized = "".join([c for c in error_msg.lower() if not c.isdigit()])
        return hashlib.md5(normalized.encode()).hexdigest()

    def is_known_failure(self, error_msg: str) -> bool:
        """Checks if the failure mode has been encountered before."""
        f_hash = self.generate_failure_hash(error_msg)
        return f_hash in self.known_failures

    def record_lesson(self, lesson: Lesson) -> str:
        """Records a new lesson and returns the failure hash."""
        f_hash = self.generate_failure_hash(lesson.error_pattern)
        self.known_failures.add(f_hash)
        return f_hash

    def get_related_lessons(
        self, error_msg: str, all_lessons: list[Lesson]
    ) -> list[Lesson]:
        """Returns lessons that match the normalized error pattern."""
        target_hash = self.generate_failure_hash(error_msg)
        return [
            lesson
            for lesson in all_lessons
            if self.generate_failure_hash(lesson.error_pattern) == target_hash
        ]
