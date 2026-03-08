# NeuralPruningEngine

**File**: `src\classes\specialized\NeuralPruningEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 317  
**Complexity**: 13 (moderate)

## Overview

Python module containing implementation for NeuralPruningEngine.

## Classes (1)

### `NeuralPruningEngine`

Implements Bio-Digital Integration.
Integrated with PruningCore for synaptic decay and refractory periods.
Phase 268: Added Static Analysis for dead code pruning and redundancy detection.
Phase 274: Added DBSCAN clustering for interaction proximity and anomaly detection.

**Methods** (13):
- `__init__(self, fleet)`
- `record_interaction(self, agent_a, agent_b)`
- `cluster_interactions(self)`
- `perform_dead_code_analysis(self, search_root)`
- `suggest_merges(self, search_root)`
- `_discover_definitions(self, root)`
- `_is_symbol_used(self, symbol, definition_file, search_root)`
- `_get_or_create_weight(self, path_id)`
- `record_usage(self, path_id)`
- `record_performance(self, path_id, success, cost)`
- ... and 3 more methods

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `logging`
- `numpy`
- `os`
- `re`
- `src.core.base.core.PruningCore.PruningCore`
- `src.core.base.core.PruningCore.SynapticWeight`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Set`
- `typing.TYPE_CHECKING`
- ... and 1 more

---
*Auto-generated documentation*
