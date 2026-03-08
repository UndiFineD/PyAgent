#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/strategies/ChainOfThoughtStrategy.description.md

# ChainOfThoughtStrategy

**File**: `src\logic\strategies\ChainOfThoughtStrategy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 48  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for ChainOfThoughtStrategy.

## Classes (1)

### `ChainOfThoughtStrategy`

**Inherits from**: AgentStrategy

Chain-of-Thought strategy: Prompt -> Reasoning -> Response.

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
## Source: src-old/logic/strategies/ChainOfThoughtStrategy.improvements.md

# Improvements for ChainOfThoughtStrategy

**File**: `src\logic\strategies\ChainOfThoughtStrategy.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ChainOfThoughtStrategy_test.py` with pytest tests

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

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Apache 2.0 License

from src.core.base.version import VERSION
from .AgentStrategy import AgentStrategy
from typing import Dict, List, Optional, TYPE_CHECKING
import logging
from collections.abc import Callable

BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION


class ChainOfThoughtStrategy(AgentStrategy):
    """Chain-of-Thought strategy: Prompt -> Reasoning -> Response."""

    async def execute(
        self,
        prompt: str,
        context: str,
        backend_call: BackendFunction,
        system_prompt: str | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        # Step 1: Reasoning
        reasoning_prompt = (
            f"{prompt}\n\nContext:\n{context}\n\n"
            "Think step-by-step about how to solve this. "
            "List the changes needed and the reasoning behind them."
        )
        reasoning = await backend_call(reasoning_prompt, system_prompt, history)
        logging.info(f"Chain of Thought Reasoning:\n{reasoning}")

        # Step 2: Execution
        execution_prompt = (
            f"{prompt}\n\nContext:\n{context}\n\n"
            f"Based on the following reasoning:\n{reasoning}\n\n"
            "Please implement the changes. Output ONLY the final code/content."
        )

        # We append the reasoning to the history for the second call if history exists
        new_history = list(history) if history else []
        new_history.append({"role": "assistant", "content": reasoning})

        return await backend_call(execution_prompt, system_prompt, new_history)
