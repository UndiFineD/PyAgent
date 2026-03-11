r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SignalCore.description.md

# SignalCore

**File**: `src\classes\orchestration\SignalCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 21  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SignalCore.

## Classes (1)

### `SignalCore`

Pure logic for the Signal Registry.
Handles event structure and history windowing.

**Methods** (2):
- `create_event(self, signal_name, data, sender)`
- `prune_history(self, history, limit)`

## Dependencies

**Imports** (5):
- `datetime.datetime`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SignalCore.improvements.md

# Improvements for SignalCore

**File**: `src\classes\orchestration\SignalCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 21 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SignalCore_test.py` with pytest tests

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

from datetime import datetime
from typing import Any, Dict, List


class SignalCore:
    """Pure logic for the Signal Registry.
    Handles event structure and history windowing.
    """

    def create_event(self, signal_name: str, data: Any, sender: str) -> Dict[str, Any]:
        """Creates a standardized signal event object."""
        return {
            "signal": signal_name,
            "data": data,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
        }

    def prune_history(
        self, history: List[Dict[str, Any]], limit: int
    ) -> List[Dict[str, Any]]:
        """Returns the last N events from the signal history."""
        return history[-limit:]
