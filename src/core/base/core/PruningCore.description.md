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
