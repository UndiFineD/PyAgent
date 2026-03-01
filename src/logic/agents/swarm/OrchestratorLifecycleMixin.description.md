# OrchestratorLifecycleMixin

**File**: `src\logic\agents\swarm\OrchestratorLifecycleMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 49  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for OrchestratorLifecycleMixin.

## Classes (1)

### `OrchestratorLifecycleMixin`

Health check and graceful shutdown methods for OrchestratorAgent.

**Methods** (5):
- `enable_graceful_shutdown(self)`
- `resume_from_shutdown(self)`
- `run_health_checks(self)`
- `is_healthy(self)`
- `print_health_report(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.GracefulShutdown.GracefulShutdown`
- `src.core.base.managers.SystemManagers.HealthChecker`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.HealthStatus`

---
*Auto-generated documentation*
