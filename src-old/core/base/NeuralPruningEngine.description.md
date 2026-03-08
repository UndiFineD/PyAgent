# NeuralPruningEngine

**File**: `src\core\base\NeuralPruningEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 394  
**Complexity**: 14 (moderate)

## Overview

Python module containing implementation for NeuralPruningEngine.

## Classes (1)

### `NeuralPruningEngine`

Implements Bio-Digital Integration.
Integrated with PruningCore for synaptic decay and refractory periods.
Phase 268: Added Static Analysis for dead code pruning and redundancy detection.
Phase 274: Added DBSCAN clustering for interaction proximity and anomaly detection.

**Methods** (14):
- `__init__(self, fleet)`
- `active_synapses(self)`
- `record_interaction(self, agent_a, agent_b)`
- `cluster_interactions(self)`
- `perform_dead_code_analysis(self, search_root)`
- `suggest_merges(self, search_root)`
- `_discover_definitions(self, root)`
- `_is_symbol_used(self, symbol, definition_file, search_root)`
- `_get_or_create_weight(self, path_id)`
- `record_usage(self, path_id)`
- ... and 4 more methods

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `logging`
- `numpy`
- `os`
- `re`
- `rust_core`
- `src.core.base.Version.VERSION`
- `src.core.base.core.PruningCore.PruningCore`
- `src.core.base.core.PruningCore.SynapticWeight`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `time`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
