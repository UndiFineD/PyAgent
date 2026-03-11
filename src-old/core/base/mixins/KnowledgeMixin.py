#!/usr/bin/env python3
# Knowledge Mixin for BaseAgent
"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/KnowledgeMixin.description.md

# KnowledgeMixin

**File**: `src\\core\base\\mixins\\KnowledgeMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 87  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for KnowledgeMixin.

## Classes (1)

### `KnowledgeMixin`

Handles knowledge engines, memory, sharded storage, and templates.

**Methods** (12):
- `__init__(self, agent_name, workspace_root)`
- `take_note(self, content)`
- `get_notes(self)`
- `clear_notes(self)`
- `register_template(self, name, template)`
- `get_template(self, name)`
- `add_to_history(self, role, content)`
- `clear_history(self)`
- `get_history(self)`
- `_build_prompt_with_history(self, prompt)`
- ... and 2 more methods

## Dependencies

**Imports** (6):
- `pathlib.Path`
- `src.core.base.ShardedKnowledgeCore.ShardedKnowledgeCore`
- `src.core.knowledge.knowledge_engine.KnowledgeEngine`
- `src.logic.agents.cognitive.LongTermMemory.LongTermMemory`
- `src.logic.agents.cognitive.context.engines.GlobalContextEngine.GlobalContextEngine`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/KnowledgeMixin.improvements.md

# Improvements for KnowledgeMixin

**File**: `src\\core\base\\mixins\\KnowledgeMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 87 lines (small)  
**Complexity**: 12 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeMixin_test.py` with pytest tests

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

from pathlib import Path
from typing import Any

from src.core.base.ShardedKnowledgeCore import ShardedKnowledgeCore


class KnowledgeMixin:
    """Handles knowledge engines, memory, sharded storage, and templates."""

    def __init__(self, agent_name: str, workspace_root: Path, **kwargs: Any) -> None:
        # Knowledge Trinity initialization
        try:
            from src.core.knowledge.knowledge_engine import KnowledgeEngine

            self.knowledge = KnowledgeEngine(
                agent_id=agent_name, base_path=Path("data/agents")
            )
        except (ImportError, ModuleNotFoundError):
            self.knowledge = None

        # Memory
        try:
            from src.logic.agents.cognitive.LongTermMemory import LongTermMemory

            self.memory = LongTermMemory(agent_name=agent_name)
        except (ImportError, ModuleNotFoundError):
            self.memory = None

        self.sharded_knowledge = ShardedKnowledgeCore(base_path=Path("data/agents"))
        self._local_global_context: Any = None
        self._workspace_root = workspace_root
        self._notes: list[str] = []
        self._prompt_templates: dict[str, Any] = {}

    def take_note(self, content: str) -> None:
        """Stores a temporary note in memory."""
        self._notes.append(content)

    def get_notes(self) -> list[str]:
        return self._notes

    def clear_notes(self) -> None:
        self._notes = []

    def register_template(self, name: str, template: Any) -> None:
        self._prompt_templates[name] = template

    def get_template(self, name: str) -> Any:
        return self._prompt_templates.get(name)

    def add_to_history(self, role: str, content: str) -> None:
        if hasattr(self, "_history_manager"):
            self._history_manager.add_message(role, content)

    def clear_history(self) -> None:
        if hasattr(self, "_history_manager"):
            self._history_manager.clear()

    def get_history(self) -> list[Any]:
        if hasattr(self, "_history_manager"):
            return self._history_manager.get_messages()
        return []

    def _build_prompt_with_history(self, prompt: str) -> str:
        history = self.get_history()
        history_text = "\n".join(
            [
                f"{getattr(m, 'role', 'user')}: {getattr(m, 'content', m)}"
                for m in history
            ]
        )
        return f"{history_text}\nUSER: {prompt}"

    @property
    def global_context(self) -> Any:
        if (
            hasattr(self, "fleet")
            and self.fleet
            and hasattr(self.fleet, "global_context")
        ):
            return self.fleet.global_context
        if self._local_global_context is None:
            try:
                from src.logic.agents.cognitive.context.engines.GlobalContextEngine import (
                    GlobalContextEngine,
                )

                self._local_global_context = GlobalContextEngine(self._workspace_root)
            except (ImportError, ValueError):
                pass
        return self._local_global_context

    @global_context.setter
    def global_context(self, value: Any) -> None:
        self._local_global_context = value
