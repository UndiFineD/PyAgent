#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/TaskDecomposer.description.md

# TaskDecomposer

**File**: `src\classes\orchestration\TaskDecomposer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 31  
**Complexity**: 3 (simple)

## Overview

Engine for dynamic task decomposition.
Breaks complex user requests into granular sub-tasks for the agent fleet.

## Classes (1)

### `TaskDecomposer`

Analyzes high-level requests and generates a multi-step plan.
Shell for TaskDecomposerCore.

**Methods** (3):
- `__init__(self, fleet_manager)`
- `decompose(self, request)`
- `get_plan_summary(self, steps)`

## Dependencies

**Imports** (6):
- `TaskDecomposerCore.TaskDecomposerCore`
- `json`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/TaskDecomposer.improvements.md

# Improvements for TaskDecomposer

**File**: `src\classes\orchestration\TaskDecomposer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 31 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TaskDecomposer_test.py` with pytest tests

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

"""Engine for dynamic task decomposition.
Breaks complex user requests into granular sub-tasks for the agent fleet.
"""

import logging
from typing import Any, Dict, List

from .TaskDecomposerCore import TaskDecomposerCore


class TaskDecomposer:
    """Analyzes high-level requests and generates a multi-step plan.
    Shell for TaskDecomposerCore.
    """

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.core = TaskDecomposerCore()

    def decompose(self, request: str) -> List[Dict[str, Any]]:
        """Splits a request into a sequence of agent steps."""
        logging.info(f"Decomposing task: {request}")
        steps = self.core.generate_plan(request)
        logging.info(f"Generated {len(steps)} steps for task.")
        return steps

    def get_plan_summary(self, steps: List[Dict[str, Any]]) -> str:
        return self.core.summarize_plan(steps)
