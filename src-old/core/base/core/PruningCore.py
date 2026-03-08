"""
LLM_CONTEXT_START

## Source: src-old/core/base/core/PruningCore.description.md

# PruningCore

**File**: `src\core\base\core\PruningCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 39  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for PruningCore.

## Classes (2)

### `SynapticWeight`

Class SynapticWeight implementation.

### `PruningCore`

Pure logic for neural pruning and synaptic decay within the agent swarm.
Handles weight calculations, refractory periods, and pruning decisions.

**Methods** (4):
- `calculate_decay(self, current_weight, idle_time_sec, half_life_sec)`
- `is_in_refractory(self, weight)`
- `update_weight_on_fire(self, current_weight, success)`
- `should_prune(self, weight, threshold)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `math`
- `time`

---
*Auto-generated documentation*
## Source: src-old/core/base/core/PruningCore.improvements.md

# Improvements for PruningCore

**File**: `src\core\base\core\PruningCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 39 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: SynapticWeight

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PruningCore_test.py` with pytest tests

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

import math
import time
from dataclasses import dataclass


@dataclass
class SynapticWeight:
    agent_id: str
    weight: float  # 0.0 to 1.0
    last_fired: float
    last_fired_cycle: int = 0
    refractory_until: float = 0.0


class PruningCore:
    """Pure logic for neural pruning and synaptic decay within the agent swarm.
    Handles weight calculations, refractory periods, and pruning decisions.
    """

    def calculate_decay(
        self, current_weight: float, idle_time_sec: float, half_life_sec: float = 3600
    ) -> float:
        """Calculates logarithmic/exponential decay for a synaptic weight."""
        # weight = weight * e^(-lambda * t)
        decay_constant = math.log(2) / half_life_sec
        new_weight = current_weight * math.exp(-decay_constant * idle_time_sec)
        return max(new_weight, 0.05)  # Floor at 0.05

    def is_in_refractory(self, weight: SynapticWeight) -> bool:
        """Checks if an agent is in a synaptic refractory period (preventing rigid over-use)."""
        return time.time() < weight.refractory_until

    def update_weight_on_fire(self, current_weight: float, success: bool) -> float:
        """Updates synaptic weight based on task outcome."""
        if success:
            return min(current_weight * 1.1, 1.0)
        return max(current_weight * 0.8, 0.1)

    def should_prune(self, weight: float, threshold: float = 0.15) -> bool:
        """Determines if a synaptic path should be pruned (deleted)."""
        return weight < threshold
