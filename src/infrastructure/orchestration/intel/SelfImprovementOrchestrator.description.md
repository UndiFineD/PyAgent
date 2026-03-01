# SelfImprovementOrchestrator

**File**: `src\infrastructure\orchestration\intel\SelfImprovementOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 86  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for SelfImprovementOrchestrator.

## Classes (1)

### `SelfImprovementOrchestrator`

**Inherits from**: BaseAgent, OrchestratorCycleMixin, OrchestratorScanMixin, OrchestratorResultsMixin

Orchestrates the fleet's self-improvement cycle: scanning for tech debt,
security leaks, and quality issues, and applying autonomous fixes.

**Methods** (1):
- `__init__(self, fleet_manager)`

## Dependencies

**Imports** (18):
- `SelfImprovementAnalysis.SelfImprovementAnalysis`
- `SelfImprovementFixer.SelfImprovementFixer`
- `__future__.annotations`
- `mixins.OrchestratorCycleMixin.OrchestratorCycleMixin`
- `mixins.OrchestratorResultsMixin.OrchestratorResultsMixin`
- `mixins.OrchestratorScanMixin.OrchestratorScanMixin`
- `os`
- `pathlib.Path`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.infrastructure.backend.LLMClient.LLMClient`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `src.infrastructure.orchestration.core.SelfImprovementCore.SelfImprovementCore`
- `src.infrastructure.orchestration.intel.SelfImprovementAnalysis.SelfImprovementAnalysis`
- ... and 3 more

---
*Auto-generated documentation*
