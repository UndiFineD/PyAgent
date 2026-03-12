#!/usr/bin/env python3
# Governance Mixin for BaseAgent
"""LLM_CONTEXT_START

## Source: src-old/core/base/mixins/GovernanceMixin.description.md

# GovernanceMixin

**File**: `src\\core\base\\mixins\\GovernanceMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 63  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for GovernanceMixin.

## Classes (1)

### `GovernanceMixin`

Handles resource quotas, preemption, and security clearance.

**Methods** (3):
- `__init__(self, config)`
- `suspend(self)`
- `resume(self)`

## Dependencies

**Imports** (6):
- `asyncio`
- `logging`
- `src.core.base.managers.ResourceQuotaManager.QuotaConfig`
- `src.core.base.managers.ResourceQuotaManager.ResourceQuotaManager`
- `src.logic.agents.security.FirewallAgent.FirewallAgent`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/GovernanceMixin.improvements.md

# Improvements for GovernanceMixin

**File**: `src\\core\base\\mixins\\GovernanceMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 63 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GovernanceMixin_test.py` with pytest tests

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

import asyncio
import logging
from typing import Any

from src.core.base.managers.ResourceQuotaManager import (
    QuotaConfig,
    ResourceQuotaManager,
)


class GovernanceMixin:
    """Handles resource quotas, preemption, and security clearance."""

    def __init__(self, config: Any, **kwargs: Any) -> None:
        self.quotas = ResourceQuotaManager(
            config=QuotaConfig(
                max_tokens=getattr(config, "max_tokens_per_session", None),
                max_time_seconds=getattr(config, "max_time_per_session", None),
            )
        )
        self._suspended: bool = False

    async def _check_preemption(self) -> None:
        while self._suspended:
            await asyncio.sleep(0.5)

    def suspend(self) -> None:
        self._suspended = True

    def resume(self) -> None:
        self._suspended = False

    async def _request_firewall_clearance(self, thought: str) -> bool:
        """Inform fleet of thought and wait for FirewallAgent clearance."""
        # Check for clearance (avoid recursion for FirewallAgent)
        if self.__class__.__name__ == "FirewallAgent":
            return True

        registry = getattr(self, "registry", None)
        if not registry and hasattr(self, "fleet") and self.fleet:
            registry = getattr(self.fleet, "signals", None)

        if registry:
            try:
                await registry.emit(
                    "thought_stream",
                    {"agent": self.__class__.__name__, "thought": thought},
                )
            except Exception as e:
                logging.debug(f"Thought emission failed: {e}")

        try:
            from src.logic.agents.security.FirewallAgent import FirewallAgent

            firewall = None
            if hasattr(self, "fleet") and self.fleet:
                firewall = self.fleet.agents.get("FirewallAgent")

            if not firewall:
                firewall = FirewallAgent()

            return await firewall.request_clearance_blocking(
                self.__class__.__name__, thought
            )
        except Exception as e:
            logging.debug(f"Firewall clearance defaulted to True (Error: {e})")
            return True
