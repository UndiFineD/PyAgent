# OrchestratorFeatures

**File**: `src\logic\agents\swarm\OrchestratorFeatures.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 39  
**Complexity**: 0 (simple)

## Overview

OrchestratorFeatures: Mixin class for OrchestratorAgent features.

## Classes (1)

### `OrchestratorFeatures`

**Inherits from**: OrchestratorPluginMixin, OrchestratorResourceMixin, OrchestratorDiffMixin, OrchestratorLifecycleMixin, OrchestratorExecutionMixin

Mixin class that provides additional features to OrchestratorAgent.
This helps keep the main OrchestratorAgent file small (<30KB).

## Dependencies

**Imports** (6):
- `OrchestratorDiffMixin.OrchestratorDiffMixin`
- `OrchestratorExecutionMixin.OrchestratorExecutionMixin`
- `OrchestratorLifecycleMixin.OrchestratorLifecycleMixin`
- `OrchestratorPluginMixin.OrchestratorPluginMixin`
- `OrchestratorResourceMixin.OrchestratorResourceMixin`
- `__future__.annotations`

---
*Auto-generated documentation*
