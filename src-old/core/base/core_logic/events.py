# Copyright 2026 PyAgent Authors
"""
LLM_CONTEXT_START

## Source: src-old/core/base/core_logic/events.description.md

# events

**File**: `src\core\base\core_logic\events.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 32  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for events.

## Classes (1)

### `EventCore`

Class EventCore implementation.

**Methods** (4):
- `trigger_event(self, event, data, hooks)`
- `filter_events(self, events, event_type)`
- `format_history_for_prompt(self, history)`
- `build_prompt_with_history(self, prompt, history, system_prompt)`

## Dependencies

**Imports** (8):
- `logging`
- `src.core.base.models.ConversationMessage`
- `src.core.base.models.EventType`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/core_logic/events.improvements.md

# Improvements for events

**File**: `src\core\base\core_logic\events.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: EventCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `events_test.py` with pytest tests

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

import logging
from typing import Any, Dict, List, Optional, Callable
from src.core.base.models import EventType, ConversationMessage

logger = logging.getLogger(__name__)


class EventCore:
    def trigger_event(
        self,
        event: EventType,
        data: dict[str, Any],
        hooks: list[Callable[[dict[str, Any]], None]],
    ) -> None:
        """Trigger an event and invoke provided hooks."""
        for callback in hooks:
            try:
                callback(data)
            except Exception as e:
                logger.warning(f"Hook error for {event.value}: {e}")

    def filter_events(
        self, events: List[Dict[str, Any]], event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filter events based on type."""
        if not event_type:
            return events
        return [e for e in events if e.get("type") == event_type]

    def format_history_for_prompt(
        self, history: list[ConversationMessage]
    ) -> list[dict[str, str]]:
        """Converts internal history objects to dicts for backend consumption."""
        return [{"role": m.role.value, "content": m.content} for m in history]

    def build_prompt_with_history(
        self, prompt: str, history: list[ConversationMessage], system_prompt: str
    ) -> str:
        """Logic to assemble the full prompt string."""
        full_prompt = f"System: {system_prompt}\n\n"
        for msg in history:
            full_prompt += f"{msg.role.name}: {msg.content}\n"
        full_prompt += f"User: {prompt}\n"
        return full_prompt
