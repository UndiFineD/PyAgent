# FleetLookupMixin

**File**: `src\infrastructure\fleet\mixins\FleetLookupMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 14 imports  
**Lines**: 136  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for FleetLookupMixin.

## Classes (1)

### `FleetLookupMixin`

Mixin for lazy loading lookups and property accessors in FleetManager.

**Methods** (12):
- `__getattr__(self, name)`
- `telemetry(self)`
- `registry(self)`
- `signals(self)`
- `recorder(self)`
- `sql_metadata(self)`
- `self_healing(self)`
- `self_improvement(self)`
- `global_context(self)`
- `fallback(self)`
- ... and 2 more methods

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `logging`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `src.infrastructure.backend.SqlMetadataHandler.SqlMetadataHandler`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `src.infrastructure.orchestration.healing.SelfHealingOrchestrator.SelfHealingOrchestrator`
- `src.infrastructure.orchestration.intel.SelfImprovementOrchestrator.SelfImprovementOrchestrator`
- `src.infrastructure.orchestration.signals.SignalRegistry.SignalRegistry`
- `src.infrastructure.orchestration.system.ToolRegistry.ToolRegistry`
- `src.logic.agents.cognitive.context.engines.GlobalContextEngine.GlobalContextEngine`
- `src.observability.stats.MetricsEngine.ModelFallbackEngine`
- `src.observability.stats.MetricsEngine.ObservabilityEngine`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
