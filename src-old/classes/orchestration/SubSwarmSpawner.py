#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/SubSwarmSpawner.description.md

# SubSwarmSpawner

**File**: `src\classes\orchestration\SubSwarmSpawner.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 68  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for SubSwarmSpawner.

## Classes (2)

### `SubSwarm`

A lightweight sub-swarm with a subset of capabilities.

**Methods** (2):
- `__init__(self, swarm_id, agents, parent_fleet)`
- `execute_mini_task(self, task)`

### `SubSwarmSpawner`

Implements Autonomous Sub-Swarm Spawning (Phase 33).
Allows the fleet to spawn specialized mini-swarms for micro-tasks.

**Methods** (4):
- `__init__(self, fleet)`
- `spawn_sub_swarm(self, capabilities)`
- `list_sub_swarms(self)`
- `get_sub_swarm(self, swarm_id)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `src.classes.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/SubSwarmSpawner.improvements.md

# Improvements for SubSwarmSpawner

**File**: `src\classes\orchestration\SubSwarmSpawner.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 68 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SubSwarmSpawner_test.py` with pytest tests

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

import logging
import uuid
from src.classes.fleet.FleetManager import FleetManager
from typing import Dict, List, Any, Optional, TYPE_CHECKING

class SubSwarm:
    """A lightweight sub-swarm with a subset of capabilities."""

    def __init__(
        self, swarm_id: str, agents: List[str], parent_fleet: FleetManager
    ) -> None:
        self.swarm_id = swarm_id
        self.agents = agents
        self.fleet = parent_fleet
        self.task_log: List[str] = []

    def execute_mini_task(self, task: str) -> str:
        logging.info(f"SubSwarm {self.swarm_id}: Executing mini-task: {task}")
        if not self.agents:
            return "Error: Sub-swarm has no agents."

        # We try to find a tool that matches the requested agent/capability
        agent_name = self.agents[0]
        try:
            # We use call_by_capability with the agent name as the goal
            result = self.fleet.call_by_capability(
                agent_name, input_text=task, technical_report=task, user_query=task
            )
            self.task_log.append(task)
            return result
        except Exception as e:
            return f"SubSwarm execution failed: {e}"


class SubSwarmSpawner:
    """
    Implements Autonomous Sub-Swarm Spawning (Phase 33).
    Allows the fleet to spawn specialized mini-swarms for micro-tasks.
    """

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.active_sub_swarms: Dict[str, SubSwarm] = {}

    def spawn_sub_swarm(self, capabilities: List[str]) -> str:
        """
        Creates a new sub-swarm based on requested capabilities or agent names.
        """
        swarm_id = f"swarm_{uuid.uuid4().hex[:8]}"
        logging.info(
            f"SubSwarmSpawner: Spawning sub-swarm {swarm_id} with {capabilities}"
        )

        # In a real system, we'd filter fleet agents by capability
        # For now, we assume provide agent names
        new_swarm = SubSwarm(swarm_id, capabilities, self.fleet)
        self.active_sub_swarms[swarm_id] = new_swarm

        if hasattr(self.fleet, "signals"):
            self.fleet.signals.emit(
                "SUB_SWARM_SPAWNED", {"swarm_id": swarm_id, "agents": capabilities}
            )

        return swarm_id

    def list_sub_swarms(self) -> List[str]:
        return list(self.active_sub_swarms.keys())

    def get_sub_swarm(self, swarm_id: str) -> Optional[SubSwarm]:
        return self.active_sub_swarms.get(swarm_id)
