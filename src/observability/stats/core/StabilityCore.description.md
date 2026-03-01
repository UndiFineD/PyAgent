# StabilityCore

**File**: `src\observability\stats\core\StabilityCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 43  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for StabilityCore.

## Classes (2)

### `FleetMetrics`

Class FleetMetrics implementation.

### `StabilityCore`

Pure logic for calculating fleet stability and reasoning coherence.
Integrates SAE activation metrics and error trends into a unified score.

**Methods** (3):
- `calculate_stability_score(self, metrics, sae_anomalies)`
- `is_in_stasis(self, score_history)`
- `get_healing_threshold(self, stability_score)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.List`

---
*Auto-generated documentation*
