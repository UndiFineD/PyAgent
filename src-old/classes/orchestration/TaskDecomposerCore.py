"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/TaskDecomposerCore.description.md

# TaskDecomposerCore

**File**: `src\classes\orchestration\TaskDecomposerCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 35  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for TaskDecomposerCore.

## Classes (1)

### `TaskDecomposerCore`

Pure logic for task decomposition.
Handles heuristic-based planning and plan summarization.

**Methods** (2):
- `generate_plan(self, request)`
- `summarize_plan(self, steps)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/TaskDecomposerCore.improvements.md

# Improvements for TaskDecomposerCore

**File**: `src\classes\orchestration\TaskDecomposerCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 35 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TaskDecomposerCore_test.py` with pytest tests

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

from typing import List, Dict, Any


class TaskDecomposerCore:
    """
    Pure logic for task decomposition.
    Handles heuristic-based planning and plan summarization.
    """

    def generate_plan(self, request: str) -> List[Dict[str, Any]]:
        """Core planning logic."""
        request_lower = request.lower()
        steps = []

        # Heuristic rules
        if "analyze" in request_lower or "data" in request_lower:
            steps.append(
                {"agent": "DataAgent", "action": "analyze_csv", "args": ["data.csv"]}
            )

        if "code" in request_lower or "refactor" in request_lower:
            steps.append(
                {
                    "agent": "CoderAgent",
                    "action": "improve_content",
                    "args": ["# code here"],
                }
            )

        if "research" in request_lower or "search" in request_lower:
            steps.append(
                {
                    "agent": "ResearchAgent",
                    "action": "search_and_summarize",
                    "args": [request],
                }
            )

        # Default fallback
        if not steps:
            steps.append(
                {"agent": "KnowledgeAgent", "action": "scan_workspace", "args": ["/"]}
            )

        return steps

    def summarize_plan(self, steps: List[Dict[str, Any]]) -> str:
        """Core summary logic."""
        summary_lines = ["Plan:"]
        for i, step in enumerate(steps):
            summary_lines.append(f"{i+1}. {step.get('agent')} -> {step.get('action')}")
        return "\n".join(summary_lines)
