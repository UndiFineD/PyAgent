r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/StatusManager.description.md

# StatusManager

**File**: `src\classes\orchestration\StatusManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 75  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for StatusManager.

## Classes (1)

### `StatusManager`

Manages project execution status for the DirectorAgent and GUI.

**Methods** (8):
- `__init__(self)`
- `clear_status(self)`
- `start_project(self, goal, steps_count)`
- `add_step(self, agent, file, prompt)`
- `update_step_status(self, index, status, result)`
- `finish_project(self, success)`
- `_read(self)`
- `_write(self, data)`

## Dependencies

**Imports** (7):
- `datetime.datetime`
- `json`
- `os`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/StatusManager.improvements.md

# Improvements for StatusManager

**File**: `src\classes\orchestration\StatusManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 75 lines (small)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StatusManager_test.py` with pytest tests

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

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class StatusManager:
    """Manages project execution status for the DirectorAgent and GUI."""

    def __init__(self) -> None:
        self.status_file = Path("src/classes/orchestration/status.json")
        self.clear_status()

    def clear_status(self) -> None:
        """Resets the status file."""
        initial_data = {
            "last_updated": datetime.now().isoformat(),
            "active_project": None,
            "steps": [],
            "current_step_index": -1,
            "overall_status": "Idle",
        }
        self._write(initial_data)

    def start_project(self, goal: str, steps_count: int) -> None:
        """Initializes a new project tracking session."""
        data = {
            "last_updated": datetime.now().isoformat(),
            "active_project": goal,
            "steps": [],
            "current_step_index": 0,
            "overall_status": "Running",
        }
        self._write(data)

    def add_step(self, agent: str, file: str, prompt: str) -> None:
        """Adds a scheduled step to the plan."""
        data = self._read()
        data["steps"].append(
            {
                "agent": agent,
                "file": file,
                "prompt": prompt,
                "status": "Pending",
                "result": None,
            }
        )
        self._write(data)

    def update_step_status(self, index: int, status: str, result: Any = None) -> None:
        """Updates the status of a specific step."""
        data = self._read()
        if 0 <= index < len(data["steps"]):
            data["steps"][index]["status"] = status
            if result:
                data["steps"][index]["result"] = result
            data["current_step_index"] = index
            data["last_updated"] = datetime.now().isoformat()
            self._write(data)

    def finish_project(self, success: bool = True) -> None:
        """Marks the project as complete."""
        data = self._read()
        data["overall_status"] = "Completed" if success else "Failed"
        data["last_updated"] = datetime.now().isoformat()
        self._write(data)

    def _read(self) -> Dict[str, Any]:
        if not self.status_file.exists():
            self.clear_status()
        with open(self.status_file, "r") as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]) -> None:
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.status_file, "w") as f:
            json.dump(data, f, indent=4)
