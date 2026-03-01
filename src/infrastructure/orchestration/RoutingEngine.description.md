# RoutingEngine

**File**: `src\infrastructure\orchestration\RoutingEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 65  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for RoutingEngine.

## Classes (1)

### `RoutingEngine`

Phase 248: PERFORMANCE-BASED ROUTING
Phase 300: FEDERATED SOVEREIGNTY ROUTING
Weights latency (TTFT/TPS) vs. quality to route tasks to the optimal provider.
Now supports routing to external federated clusters.

**Methods** (3):
- `__init__(self)`
- `select_provider(self, task_type, priority, federated)`
- `get_routing_stats()`

## Dependencies

**Imports** (5):
- `logging`
- `os`
- `src.infrastructure.backend.RunnerBackends.BackendHandlers`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
