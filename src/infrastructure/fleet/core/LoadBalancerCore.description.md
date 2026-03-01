# LoadBalancerCore

**File**: `src\infrastructure\fleet\core\LoadBalancerCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for LoadBalancerCore.

## Classes (2)

### `AgentMetrics`

Class AgentMetrics implementation.

### `LoadBalancerCore`

Pure logic for cognitive load balancing across the agent fleet.
Calculates cognitive pressure and suggests optimal task routing.

**Methods** (3):
- `calculate_cognitive_pressure(self, metrics)`
- `select_best_agent(self, agents)`
- `suggest_scaling(self, fleet_pressure)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.Dict`

---
*Auto-generated documentation*
