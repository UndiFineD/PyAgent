#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SignalAgent.description.md

# SignalAgent

**File**: `src\classes\orchestration\SignalAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 59  
**Complexity**: 5 (moderate)

## Overview

Agent that monitor inter-agent signals and coordinates responses.

## Classes (1)

### `SignalAgent`

**Inherits from**: BaseAgent

Monitors the SignalRegistry and triggers actions based on events.

**Methods** (5):
- `__init__(self, file_path)`
- `_get_default_content(self)`
- `on_agent_fail(self, event)`
- `on_improvement_ready(self, event)`
- `get_signal_summary(self)`

## Dependencies

**Imports** (8):
- `SignalRegistry.SignalRegistry`
- `json`
- `logging`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SignalAgent.improvements.md

# Improvements for SignalAgent

**File**: `src\classes\orchestration\SignalAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 59 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SignalAgent_test.py` with pytest tests

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

"""Agent that monitor inter-agent signals and coordinates responses."""

from src.classes.base_agent import BaseAgent
from .SignalRegistry import SignalRegistry
import logging
import json
from typing import Dict, List, Any, Optional


class SignalAgent(BaseAgent):
    """Monitors the SignalRegistry and triggers actions based on events."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.registry = SignalRegistry()

        # Subscribe to all signals to log them
        # In a real app, it would only subscribe to specific ones
        self.registry.subscribe("agent_fail", self.on_agent_fail)
        self.registry.subscribe("improvement_ready", self.on_improvement_ready)

        self._system_prompt = (
            "You are the Signal Agent (Event Coordinator). "
            "You watch the system's pulse (signals) and suggest interventions. "
            "If an agent fails consistently, you flag it for review. "
            "If a new improvement is ready, you notify the Director."
        )

    def _get_default_content(self) -> str:
        return "# Signal Observation Log\n\n## Events\nNo recent events.\n"

    def on_agent_fail(self, event: Dict[str, Any]) -> str:
        """Handle an agent failure signal."""
        sender = event.get("sender")
        data = event.get("data")
        logging.warning(f"SignalAgent handling failure from {sender}: {data}")
        # Append to log
        self.append_to_file(
            f"\n- [!] {event['timestamp']} Agent **{sender}** failed: {data}"
        )

    def on_improvement_ready(self, event: Dict[str, Any]) -> str:
        """Handle a new improvement signal."""
        data = event.get("data")
        logging.info(f"SignalAgent noticing new improvement: {data}")
        self.append_to_file(
            f"\n- [i] {event['timestamp']} New improvement proposed: {data}"
        )

    def get_signal_summary(self) -> str:
        """Return a formatted summary of recent signals."""
        history = self.registry.get_history(10)
        if not history:
            return "No signals recorded yet."

        summary = ["## Recent System Signals"]
        for h in history:
            summary.append(
                f"- **{h['signal']}** from {h['sender']} at {h['timestamp']}"
            )
            if h["data"]:
                summary.append(f"  - Data: `{json.dumps(h['data'])[:100]}`")

        return "\n".join(summary)
