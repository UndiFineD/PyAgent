#!/usr/bin/env python3

"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/ScalingManager.description.md

# ScalingManager

**File**: `src\\classes\fleet\\ScalingManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 42  
**Complexity**: 4 (simple)

## Overview

Manager for dynamic scaling of the agent fleet.
Monitors system load and spawns new agent instances as needed.

## Classes (1)

### `ScalingManager`

Shell for ScalingManager.
Handles fleet orchestration while delegating logic to ScalingCore.

**Methods** (4):
- `__init__(self, fleet_manager)`
- `record_metric(self, agent_name, latency)`
- `_execute_scale_out(self, agent_name)`
- `get_scaling_status(self)`

## Dependencies

**Imports** (8):
- `ScalingCore.ScalingCore`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Type`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/ScalingManager.improvements.md

# Improvements for ScalingManager

**File**: `src\\classes\fleet\\ScalingManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 42 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ScalingManager_test.py` with pytest tests

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

"""Manager for dynamic scaling of the agent fleet.
Monitors system load and spawns new agent instances as needed.
"""

import logging
import time

from .ScalingCore import ScalingCore


class ScalingManager:
    """Shell for ScalingManager.
    Handles fleet orchestration while delegating logic to ScalingCore.
    """

    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.core = ScalingCore(scale_threshold=5.0, window_size=10)

    def record_metric(self, agent_name: str, latency: float) -> None:
        """Records the latency and checks if scaling is required."""
        self.core.add_metric(agent_name, latency)

        if self.core.should_scale(agent_name):
            self._execute_scale_out(agent_name)

    def _execute_scale_out(self, agent_name: str) -> None:
        """Spawns a new instance of an agent if latency is too high."""
        avg_latency = self.core.get_avg_latency(agent_name)
        logging.warning(
            f"SCALING: High latency ({avg_latency:.2f}s) detected for {agent_name}. Spawning replica."
        )

        # Replica naming logic
        replica_name = f"{agent_name}_replica_{int(time.time())}"
        # Implementation depends on FleetManager dynamic registration
        if hasattr(self.fleet, "register_agent_runtime"):
            self.fleet.register_agent_runtime(replica_name, agent_name)

    def get_scaling_status(self) -> str:
        """Returns the current scaling status."""
        return f"Scaling Manager: Monitoring {len(self.core.load_metrics)} agent types."
