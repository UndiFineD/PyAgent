#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SelfHealingEngine.description.md

# SelfHealingEngine

**File**: `src\classes\orchestration\SelfHealingEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 40  
**Complexity**: 3 (simple)

## Overview

Engine for automated self-repair of agent tools and modules.
Detects runtime errors and orchestrates CoderAgents to apply fixes.

## Classes (1)

### `SelfHealingEngine`

Monitors tool execution and attempts automatic fixes for crashes.
Shell for SelfHealingEngineCore.

**Methods** (3):
- `__init__(self, workspace_root)`
- `handle_failure(self, agent, tool_name, error, context)`
- `get_healing_stats(self)`

## Dependencies

**Imports** (9):
- `SelfHealingEngineCore.SelfHealingEngineCore`
- `logging`
- `src.classes.base_agent.BaseAgent`
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SelfHealingEngine.improvements.md

# Improvements for SelfHealingEngine

**File**: `src\classes\orchestration\SelfHealingEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SelfHealingEngine_test.py` with pytest tests

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

"""Engine for automated self-repair of agent tools and modules.
Detects runtime errors and orchestrates CoderAgents to apply fixes.
"""

import logging
import traceback
from typing import Any, Dict, List

from src.classes.base_agent import BaseAgent

from .SelfHealingEngineCore import SelfHealingEngineCore


class SelfHealingEngine:
    """Monitors tool execution and attempts automatic fixes for crashes.
    Shell for SelfHealingEngineCore.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root
        self.failure_history: List[Dict[str, Any]] = []
        self.core = SelfHealingEngineCore()

    def handle_failure(self, agent: BaseAgent, tool_name: str, error: Exception, context: Dict[str, Any]) -> str:
        """Analyzes a failure and attempts to generate a fix."""
        tb = traceback.format_exc()
        agent_name = agent.__class__.__name__
        logging.error(f"SELF-HEAL: Failure in {agent_name}.{tool_name}: {error}\n{tb}")

        analysis = self.core.analyze_failure(agent_name, tool_name, str(error), tb)
        analysis["context"] = context
        self.failure_history.append(analysis)

        # Fixed logic: communicate strategy
        return f"Self-Healing initiated: Strategy '{analysis['strategy']}' assigned to {tool_name}."

    def get_healing_stats(self) -> str:
        """Returns a summary of healing attempts."""
        return self.core.format_healing_report(self.failure_history)
