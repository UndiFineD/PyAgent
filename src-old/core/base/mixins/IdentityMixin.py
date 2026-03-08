#!/usr/bin/env python3
# Identity Mixin for BaseAgent
"""
LLM_CONTEXT_START

## Source: src-old/core/base/mixins/IdentityMixin.description.md

# IdentityMixin

**File**: `src\core\base\mixins\IdentityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 49  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for IdentityMixin.

## Classes (1)

### `IdentityMixin`

Handles agent identity, configuration, and capabilities.

**Methods** (3):
- `__init__(self)`
- `get_capabilities(self)`
- `_register_capabilities(self)`

## Dependencies

**Imports** (4):
- `asyncio`
- `src.core.base.models.AgentPriority`
- `src.infrastructure.orchestration.signals.SignalRegistry.SignalRegistry`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/IdentityMixin.improvements.md

# Improvements for IdentityMixin

**File**: `src\core\base\mixins\IdentityMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 49 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `IdentityMixin_test.py` with pytest tests

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

from typing import Any
from src.core.base.models import AgentPriority


class IdentityMixin:
    """Handles agent identity, configuration, and capabilities."""

    def __init__(self, **kwargs: Any) -> None:
        self.agent_name = self.__class__.__name__.lower().replace("agent", "") or "base"
        self.capabilities: list[str] = ["base"]
        self.priority: AgentPriority = kwargs.get("priority", AgentPriority.NORMAL)
        self._suspended: bool = False

    def get_capabilities(self) -> list[str]:
        return self.capabilities

    def _register_capabilities(self) -> None:
        """Emits a signal with agent capabilities for discovery."""
        try:
            import asyncio
            from src.infrastructure.orchestration.signals.SignalRegistry import (
                SignalRegistry,
            )

            signals = SignalRegistry()
            # Note: We expect the class using this mixin to have agent_logic_core
            if hasattr(self, "agent_logic_core"):
                payload = self.agent_logic_core.prepare_capability_payload(
                    self.__class__.__name__, self.get_capabilities()
                )

                try:
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    if loop.is_running():
                        asyncio.create_task(
                            signals.emit("agent_capability_registration", payload)
                        )
                    else:
                        loop.run_until_complete(
                            signals.emit("agent_capability_registration", payload)
                        )
                except Exception:
                    pass
        except Exception:
            pass
