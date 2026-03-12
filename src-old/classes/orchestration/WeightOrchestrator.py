#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/orchestration/WeightOrchestrator.description.md

# WeightOrchestrator

**File**: `src\classes\orchestration\WeightOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 79  
**Complexity**: 8 (moderate)

## Overview

WeightOrchestrator for PyAgent.
Manages the lifecycle of neural weights (LoRA/QLoRA adapters) across the fleet.
Coordinates between the ModelForgeAgent and individual agents to hot-swap capabilities.

## Classes (1)

### `WeightOrchestrator`

**Inherits from**: BaseAgent

Orchestrates the distribution and activation of model weights across the fleet.

**Methods** (8):
- `__init__(self, file_path)`
- `_load_registry(self)`
- `_save_registry(self)`
- `activate_adapter(self, agent_name, adapter_name)`
- `get_active_adapter(self, agent_name)`
- `deactivate_adapter(self, agent_name)`
- `list_registrations(self)`
- `improve_content(self, input_text)`

## Dependencies

**Imports** (9):
- `json`
- `logging`
- `pathlib.Path`
- `src.classes.base_agent.BaseAgent`
- `src.classes.base_agent.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/WeightOrchestrator.improvements.md

# Improvements for WeightOrchestrator

**File**: `src\classes\orchestration\WeightOrchestrator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 79 lines (small)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `WeightOrchestrator_test.py` with pytest tests

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

"""WeightOrchestrator for PyAgent.
Manages the lifecycle of neural weights (LoRA/QLoRA adapters) across the fleet.
Coordinates between the ModelForgeAgent and individual agents to hot-swap capabilities.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool


class WeightOrchestrator(BaseAgent):
    """Orchestrates the distribution and activation of model weights across the fleet."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = Path(file_path).parent
        self.weights_registry_path = (
            self.workspace_root / "data/agents/store/weights_registry.json"
        )
        self.active_adapters: Dict[str, str] = {}  # agent_name -> adapter_name
        self._load_registry()
        self._system_prompt = "You are the Weight Orchestrator. You manage model adapters and neural weights across the fleet."

    def _load_registry(self) -> bool:
        if self.weights_registry_path.exists():
            try:
                with open(self.weights_registry_path, "r") as f:
                    data = json.load(f)
                    self.active_adapters = data.get("active_adapters", {})
            except Exception as e:
                logging.error(f"WeightOrchestrator: Failed to load registry: {e}")

    def _save_registry(self) -> bool:
        try:
            self.weights_registry_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.weights_registry_path, "w") as f:
                json.dump({"active_adapters": self.active_adapters}, f, indent=4)
        except Exception as e:
            logging.error(f"WeightOrchestrator: Failed to save registry: {e}")

    @as_tool
    def activate_adapter(self, agent_name: str, adapter_name: str) -> bool:
        """Assigns an adapter to an agent and triggers a 'weights_updated' signal."""
        logging.info(
            f"WeightOrchestrator: Activating adapter '{adapter_name}' for agent '{agent_name}'"
        )
        self.active_adapters[agent_name] = adapter_name
        self._save_registry()
        # In a real system, this would trigger a signal that the agent's Proxy or Backend listens to
        return True

    @as_tool
    def get_active_adapter(self, agent_name: str) -> Optional[str]:
        """Returns the currently active adapter for an agent."""
        return self.active_adapters.get(agent_name)

    @as_tool
    def deactivate_adapter(self, agent_name: str) -> bool:
        """Removes the active adapter from an agent."""
        if agent_name in self.active_adapters:
            del self.active_adapters[agent_name]
            self._save_registry()
            return True
        return False

    @as_tool
    def list_registrations(self) -> Dict[str, str]:
        """Returns all current agent-to-adapter mappings."""
        return self.active_adapters

    def improve_content(self, input_text: str) -> str:
        return f"Current fleet weight distribution: {len(self.active_adapters)} active adapters."


if __name__ == "__main__":
    # Internal test
    orchestrator = WeightOrchestrator(".")
    orchestrator.activate_adapter("LinguisticAgent", "poetry_v1")
    print(f"Active adapters: {orchestrator.list_registrations()}")
