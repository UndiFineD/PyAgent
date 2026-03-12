#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SignalBusOrchestrator.description.md

# SignalBusOrchestrator

**File**: `src\classes\orchestration\SignalBusOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 53  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for SignalBusOrchestrator.

## Classes (1)

### `SignalBusOrchestrator`

High-speed signal bus for low-latency agent-to-agent communication.
Uses an internal message queue and a pub-sub pattern to bypass slow JSON/HTTP overhead.

**Methods** (5):
- `__init__(self)`
- `subscribe(self, signal_type, callback)`
- `publish(self, signal_type, payload, sender)`
- `_process_bus(self)`
- `shutdown(self)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `queue`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SignalBusOrchestrator.improvements.md

# Improvements for SignalBusOrchestrator

**File**: `src\classes\orchestration\SignalBusOrchestrator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 53 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SignalBusOrchestrator_test.py` with pytest tests

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

import logging
import queue
import threading
from typing import Any, Callable, Dict, List


class SignalBusOrchestrator:
    """High-speed signal bus for low-latency agent-to-agent communication.
    Uses an internal message queue and a pub-sub pattern to bypass slow JSON/HTTP overhead.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}
        self._queue = queue.Queue()
        self._running = True
        self._thread = threading.Thread(target=self._process_bus, daemon=True)
        self._thread.start()

    def subscribe(self, signal_type: str, callback: Callable) -> None:
        """Registers a callback for a specific signal type."""
        if signal_type not in self._subscribers:
            self._subscribers[signal_type] = []
        self._subscribers[signal_type].append(callback)
        logging.debug(f"SignalBus: Subscribed to '{signal_type}'")

    def publish(self, signal_type: str, payload: Any, sender: str = "System") -> None:
        """Publishes a signal to the bus."""
        self._queue.put({"type": signal_type, "payload": payload, "sender": sender})

    def _process_bus(self) -> None:
        """Internal loop to process signals asynchronously."""
        while self._running:
            try:
                msg = self._queue.get(timeout=1.0)
                signal_type = msg["type"]
                if signal_type in self._subscribers:
                    for callback in self._subscribers[signal_type]:
                        try:
                            callback(msg["payload"], msg["sender"])
                        except Exception as e:
                            logging.error(
                                f"SignalBus: Callback error for {signal_type}: {e}"
                            )
                self._queue.task_done()
            except queue.Empty:
                continue

    def shutdown(self) -> None:
        """Stops the signal bus."""
        self._running = False
        self._thread.join()
        logging.info("SignalBus: Shutdown complete.")
