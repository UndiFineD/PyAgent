#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/logic/strategies/ReflexionStrategy.description.md

# ReflexionStrategy

**File**: `src\logic\strategies\ReflexionStrategy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 49  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for ReflexionStrategy.

## Classes (1)

### `ReflexionStrategy`

**Inherits from**: AgentStrategy

Reflexion strategy: Draft -> Critique -> Revise.

## Dependencies

**Imports** (9):
- `AgentStrategy.AgentStrategy`
- `__future__.annotations`
- `collections.abc.Callable`
- `logging`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
## Source: src-old/logic/strategies/ReflexionStrategy.improvements.md

# Improvements for ReflexionStrategy

**File**: `src\logic\strategies\ReflexionStrategy.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 49 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReflexionStrategy_test.py` with pytest tests

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

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Dict, List, Optional

# Copyright 2026 PyAgent Authors
# Apache 2.0 License
from src.core.base.version import VERSION

from .AgentStrategy import AgentStrategy

BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class ReflexionStrategy(AgentStrategy):
    """Reflexion strategy: Draft -> Critique -> Revise."""

    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        # Step 1: Draft
        draft = await backend_call(
            f"{prompt}\n\nContext:\n{context}", system_prompt, history
        )

        # Step 2: Critique
        critique_prompt = (
            f"Original Request: {prompt}\n\n"
            f"Draft Implementation:\n{draft}\n\n"
            "Critique this implementation. Identify any bugs, missing requirements, "
            "or style issues. Be harsh but constructive."
        )
        critique = await backend_call(
            critique_prompt, "You are a senior code reviewer.", []
        )
        logging.info(f"Reflexion Critique:\n{critique}")

        # Step 3: Revise
        revision_prompt = (
            f"Original Request: {prompt}\n\n"
            f"Draft Implementation:\n{draft}\n\n"
            f"Critique:\n{critique}\n\n"
            "Please rewrite the implementation to address the critique. "
            "Output ONLY the final code/content."
        )
        return await backend_call(revision_prompt, system_prompt, history)
