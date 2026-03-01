# OrchestratorCycleMixin

**File**: `src\infrastructure\orchestration\intel\mixins\OrchestratorCycleMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 63  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for OrchestratorCycleMixin.

## Classes (1)

### `OrchestratorCycleMixin`

Methods for managing the improvement cycle and gates.

**Methods** (3):
- `run_improvement_cycle(self, target_dir)`
- `_check_gate_stability(self)`
- `_ingest_hive_tasks(self)`

## Dependencies

**Imports** (4):
- `logging`
- `src.core.base.Version.STABILITY_SCORE`
- `src.core.base.Version.is_gate_open`
- `typing.Any`

---
*Auto-generated documentation*
