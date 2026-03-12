#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SignalRegistry.description.md

# SignalRegistry

**File**: `src\classes\orchestration\SignalRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

A simple event-driven signal registry for inter-agent communication.

## Classes (1)

### `SignalRegistry`

Central hub for publishing and subscribing to agent signals.
Shell for SignalCore.

**Methods** (4):
- `__new__(cls)`
- `subscribe(self, signal_name, callback)`
- `emit(self, signal_name, data, sender)`
- `get_history(self, limit)`

## Dependencies

**Imports** (8):
- `SignalCore.SignalCore`
- `datetime.datetime`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SignalRegistry.improvements.md

# Improvements for SignalRegistry

**File**: `src\classes\orchestration\SignalRegistry.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SignalRegistry_test.py` with pytest tests

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

"""A simple event-driven signal registry for inter-agent communication."""

import logging
from typing import Any, Callable, Dict, List

from .SignalCore import SignalCore


class SignalRegistry:
    """Central hub for publishing and subscribing to agent signals.
    Shell for SignalCore.
    """

    _instance = None

    def __new__(cls, *args, **kwargs) -> "SignalRegistry":
        if cls._instance is None:
            cls._instance = super(SignalRegistry, cls).__new__(cls)
            cls._instance.subscribers = {} # signal_name -> list of callbacks
            cls._instance.history = []
            cls._instance.core = SignalCore()
        return cls._instance

    def subscribe(self, signal_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe a callback to a signal."""
        if signal_name not in self.subscribers:
            self.subscribers[signal_name] = []
        self.subscribers[signal_name].append(callback)
        logging.debug(f"Subscribed callback to signal: {signal_name}")

    def emit(self, signal_name: str, data: Any = None, sender: str = "system") -> None:
        """Emit a signal to all subscribers."""
        event = self.core.create_event(signal_name, data, sender)
        self.history.append(event)

        logging.info(f"Signal emitted: {signal_name} from {sender}")

        if signal_name in self.subscribers:
            for callback in self.subscribers[signal_name]:
                try:
                    callback(event)
                except Exception as e:
                    logging.error(f"Error in signal callback for {signal_name}: {e}")

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get the recent signal history."""
        return self.core.prune_history(self.history, limit)
