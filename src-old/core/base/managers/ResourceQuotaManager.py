"""
LLM_CONTEXT_START

## Source: src-old/core/base/managers/ResourceQuotaManager.description.md

# ResourceQuotaManager

**File**: `src\core\base\managers\ResourceQuotaManager.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 6 imports  
**Lines**: 88  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for ResourceQuotaManager.

## Classes (3)

### `QuotaConfig`

Configuration for agent resource quotas.

### `ResourceUsage`

Current resource usage for an agent session.

**Methods** (2):
- `total_tokens(self)`
- `elapsed_time(self)`

### `ResourceQuotaManager`

Manages resource quotas and budget enforcement for agent sessions.

Phase 245: RESOURCE QUOTAS & BUDGETS

**Methods** (6):
- `__init__(self, config)`
- `update_usage(self, tokens_input, tokens_output, cycles)`
- `check_quotas(self)`
- `is_interrupted(self)`
- `interrupt_reason(self)`
- `get_report(self)`

## Dependencies

**Imports** (6):
- `dataclasses.dataclass`
- `dataclasses.field`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/managers/ResourceQuotaManager.improvements.md

# Improvements for ResourceQuotaManager

**File**: `src\core\base\managers\ResourceQuotaManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 88 lines (small)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResourceQuotaManager_test.py` with pytest tests

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

import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class QuotaConfig:
    """Configuration for agent resource quotas."""

    max_tokens: int | None = None
    max_time_seconds: int | None = None
    max_cycles: int | None = None


@dataclass
class ResourceUsage:
    """Current resource usage for an agent session."""

    tokens_input: int = 0
    tokens_output: int = 0
    start_time: float = field(default_factory=time.time)
    cycles: int = 0

    @property
    def total_tokens(self) -> int:
        return self.tokens_input + self.tokens_output

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time


class ResourceQuotaManager:
    """Manages resource quotas and budget enforcement for agent sessions.

    Phase 245: RESOURCE QUOTAS & BUDGETS
    """

    def __init__(self, config: QuotaConfig | None = None) -> None:
        self.config = config or QuotaConfig()
        self.usage = ResourceUsage()
        self._is_interrupted = False
        self._interrupt_reason: str | None = None

    def update_usage(
        self, tokens_input: int = 0, tokens_output: int = 0, cycles: int = 0
    ) -> bool:
        """Update current usage metrics."""
        self.usage.tokens_input += tokens_input
        self.usage.tokens_output += tokens_output
        self.usage.cycles += cycles

    def check_quotas(self) -> tuple[bool, str | None]:
        """Check if any quotas have been exceeded.

        Returns:
            (is_exceeded, reason)
        """
        if self.config.max_tokens and self.usage.total_tokens >= self.config.max_tokens:
            self._is_interrupted = True
            self._interrupt_reason = f"Token quota exceeded ({self.usage.total_tokens} >= {self.config.max_tokens})"
            return True, self._interrupt_reason

        if (
            self.config.max_time_seconds
            and self.usage.elapsed_time >= self.config.max_time_seconds
        ):
            self._is_interrupted = True
            self._interrupt_reason = f"Time quota exceeded ({self.usage.elapsed_time:.2f}s >= {self.config.max_time_seconds}s)"
            return True, self._interrupt_reason

        if self.config.max_cycles and self.usage.cycles >= self.config.max_cycles:
            self._is_interrupted = True
            self._interrupt_reason = f"Cycle quota exceeded ({self.usage.cycles} >= {self.config.max_cycles})"
            return True, self._interrupt_reason

        return False, None

    @property
    def is_interrupted(self) -> bool:
        return self._is_interrupted

    @property
    def interrupt_reason(self) -> str | None:
        return self._interrupt_reason

    def get_report(self) -> dict[str, Any]:
        """Returns a summary of resource usage."""
        return {
            "tokens_input": self.usage.tokens_input,
            "tokens_output": self.usage.tokens_output,
            "total_tokens": self.usage.total_tokens,
            "elapsed_time": self.usage.elapsed_time,
            "cycles": self.usage.cycles,
            "interrupted": self._is_interrupted,
            "reason": self._interrupt_reason,
        }
