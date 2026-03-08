# cassette_mixin

**File**: `src\core\base\mixins\cassette_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 43  
**Complexity**: 3 (simple)

## Overview

Mixin regarding Synaptic Modularization (Cassette-based logic).

## Classes (1)

### `CassetteMixin`

Mixin regarding providing Cassette Orchestration capabilities to an Agent.

**Methods** (3):
- `__init__(self)`
- `register_logic_cassette(self, cassette)`
- `has_cassette(self, name)`

## Dependencies

**Imports** (5):
- `src.core.base.logic.cassette_orchestrator.BaseLogicCassette`
- `src.core.base.logic.cassette_orchestrator.CassetteOrchestrator`
- `src.core.base.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
