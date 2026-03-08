#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/WorkflowState.description.md

# WorkflowState

**File**: `src\classes\fleet\WorkflowState.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 29  
**Complexity**: 3 (simple)

## Overview

Container for shared state and context between agents in a workflow.

## Classes (1)

### `WorkflowState`

Maintains context, variables, and history for a multi-agent session.

**Methods** (3):
- `set(self, key, value)`
- `get(self, key, default)`
- `add_history(self, agent, action, result)`

## Dependencies

**Imports** (6):
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/WorkflowState.improvements.md

# Improvements for WorkflowState

**File**: `src\classes\fleet\WorkflowState.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 29 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `WorkflowState_test.py` with pytest tests

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

"""Container for shared state and context between agents in a workflow."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class WorkflowState:
    """Maintains context, variables, and history for a multi-agent session."""

    task_id: str
    original_request: str
    variables: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    context_snippets: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        self.variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)

    def add_history(self, agent: str, action: str, result: str) -> None:
        self.history.append(
            {
                "agent": agent,
                "action": action,
                "result": result[:500] + "..." if len(result) > 500 else result,
            }
        )
