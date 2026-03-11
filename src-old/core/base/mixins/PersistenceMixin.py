#!/usr/bin/env python3
# Persistence Mixin for BaseAgent
"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/PersistenceMixin.description.md

# PersistenceMixin

**File**: `src\\core\base\\mixins\\PersistenceMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 112  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for PersistenceMixin.

## Classes (1)

### `PersistenceMixin`

Handles agent state, history, scratchpad, metrics, and file persistence.

**Methods** (11):
- `__init__(self)`
- `state(self)`
- `register_webhook(self, url)`
- `_trigger_event(self, event_type, data)`
- `generate_diff(self)`
- `get_diff(self)`
- `read_previous_content(self)`
- `update_file(self)`
- `_write_dry_run_diff(self)`
- `save_state(self)`
- ... and 1 more methods

## Dependencies

**Imports** (9):
- `logging`
- `pathlib.Path`
- `src.core.base.AgentHistory.AgentConversationHistory`
- `src.core.base.AgentScratchpad.AgentScratchpad`
- `src.core.base.models.AgentState`
- `src.core.base.models.EventType`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/PersistenceMixin.improvements.md

# Improvements for PersistenceMixin

**File**: `src\\core\base\\mixins\\PersistenceMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 112 lines (medium)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PersistenceMixin_test.py` with pytest tests

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

from typing import Any, List

from src.core.base.AgentHistory import AgentConversationHistory
from src.core.base.AgentScratchpad import AgentScratchpad
from src.core.base.models import AgentState, EventType


class PersistenceMixin:
    """Handles agent state, history, scratchpad, metrics, and file persistence."""

    def __init__(self, **kwargs: Any) -> None:
        """Initializes persistence-related attributes."""
        self._state: AgentState = AgentState.INITIALIZED
        self._history_manager = AgentConversationHistory()
        self._scratchpad_manager = AgentScratchpad()
        self._webhooks: List[str] = []
        self._event_hooks: dict[EventType, list[Any]] = {}
        self._metrics_data: dict[str, Any] = {}

    @property
    def state(self) -> AgentState:
        """Current agent state."""
        return self._state

    def register_webhook(self, url: str) -> None:
        """Registers a webhook URL for notifications."""
        if url not in self._webhooks:
            self._webhooks.append(url)

    def _trigger_event(self, event_type: EventType, data: dict[str, Any]) -> None:
        """Triggers local events and hooks."""
        hooks = self._event_hooks.get(event_type, [])
        for hook in hooks:
            try:
                hook(data)
            except Exception:
                pass

    def generate_diff(self) -> str:
        """Generate a unified diff between original and improved content."""
        if (
            hasattr(self, "core")
            and hasattr(self, "previous_content")
            and hasattr(self, "current_content")
        ):
            return self.core.calculate_diff(
                self.previous_content,
                self.current_content,
                filename=str(self.file_path),
            )
        return ""

    def get_diff(self) -> str:
        """Public method to get the diff for verification."""
        return self.generate_diff()

    def read_previous_content(self) -> str:
        """Reads original file content into previous_content."""
        if not hasattr(self, "file_path") or not self.file_path.exists():
            self.previous_content = "# New Document\n"
            return self.previous_content

        try:
            self.previous_content = self.file_path.read_text(encoding="utf-8")
        except Exception:
            self.previous_content = ""
        return self.previous_content

    def update_file(self) -> bool:
        """Write content back to disk."""
        if not hasattr(self, "current_content") or not hasattr(self, "file_path"):
            return False

        content_to_write = self.current_content
        suffix = self.file_path.suffix.lower()
        if suffix in {".md", ".markdown"} or self.file_path.name.lower().endswith(
            ".plan.md"
        ):
            content_to_write = self.core.fix_markdown(content_to_write)

        if not self.core.validate_content_safety(content_to_write):
            import logging

            logging.error(f"Security violation detected in {self.file_path.name}")
            return False

        if getattr(self, "_config", None) and getattr(self._config, "dry_run", False):
            return self._write_dry_run_diff()

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text(content_to_write, encoding="utf-8")
            return True
        except Exception as e:
            import logging

            logging.error(f"File write failed: {e}")
            return False

    def _write_dry_run_diff(self) -> bool:
        """Saves a diff for verification without modifying the file."""
        from pathlib import Path

        diff = self.get_diff()
        if not diff:
            return True

        dry_run_dir = Path("temp/dry_runs")
        dry_run_dir.mkdir(parents=True, exist_ok=True)
        safe_name = self.file_path.name.replace("/", "_").replace("\\", "_")
        target = dry_run_dir / f"{safe_name}.diff"
        target.write_text(diff, encoding="utf-8")
        return True

    def save_state(self) -> bool:
        """Saves current state snapshot."""
        if hasattr(self, "agent_logic_core"):
            return self.agent_logic_core.save_state(self._state_data)
        return False

    def load_state(self) -> bool:
        """Loads state from local storage."""
        if hasattr(self, "agent_logic_core"):
            self._state_data = self.agent_logic_core.load_state()
            return True
        return False
