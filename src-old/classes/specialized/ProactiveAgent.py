#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/ProactiveAgent.description.md

# ProactiveAgent

**File**: `src\classes\specialized\ProactiveAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 59  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in proactive task management and recurring workflows (Sentient pattern).

## Classes (1)

### `ProactiveAgent`

**Inherits from**: BaseAgent

Manages recurring, triggered, and scheduled tasks proactively.

**Methods** (5):
- `__init__(self, file_path)`
- `schedule_task(self, task, cron_or_delay)`
- `scan_for_triggers(self, environment_state)`
- `get_habit_recommendation(self, user_history)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.create_main_function`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/ProactiveAgent.improvements.md

# Improvements for ProactiveAgent

**File**: `src\classes\specialized\ProactiveAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 59 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ProactiveAgent_test.py` with pytest tests

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

"""Agent specializing in proactive task management and recurring workflows (Sentient pattern)."""

from src.classes.base_agent import BaseAgent
import logging
import json
import time
from typing import Dict, List, Any, Optional


class ProactiveAgent(BaseAgent):
    """Manages recurring, triggered, and scheduled tasks proactively."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Proactive Agent. "
            "Your role is to monitor the environment and execute tasks based on triggers, "
            "schedules, or detected patterns. You don't just wait for prompts; you anticipate needs."
        )
        self.scheduled_tasks: List[Dict[str, Any]] = []

    def schedule_task(self, task: str, cron_or_delay: str) -> str:
        """Schedules a task for future execution."""
        task_entry = {
            "id": f"task_{int(time.time())}",
            "task": task,
            "trigger": cron_or_delay,
            "status": "scheduled",
        }
        self.scheduled_tasks.append(task_entry)
        logging.info(
            f"ProactiveAgent: Scheduled task '{task}' with trigger '{cron_or_delay}'"
        )
        return json.dumps(task_entry)

    def scan_for_triggers(self, environment_state: Dict[str, Any]) -> List[str]:
        """Checks if any environmental triggers should fire a proactive task."""
        triggered_tasks = []
        # Example triggers
        if environment_state.get("disk_usage", 0) > 90:
            triggered_tasks.append("Cleanup workspace: Disk usage high")
        if environment_state.get("error_count", 0) > 5:
            triggered_tasks.append("Diagnostic: High error rate detected")

        return triggered_tasks

    def get_habit_recommendation(self, user_history: List[str]) -> str:
        """Learns habits from user history and suggests optimizations."""
        if len(user_history) > 10:
            return "Observation: You frequently run tests after editing 'fleet' files. Should I automate this?"
        return "Not enough data yet to establish habits."

    def improve_content(self, input_text: str) -> str:
        """Returns proactive suggestions based on current context."""
        return self.get_habit_recommendation([])  # Placeholder


if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function

    main = create_main_function(ProactiveAgent)
    main()
