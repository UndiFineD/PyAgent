# SelfImprovementCoordinator

**File**: `src\maintenance\SelfImprovementCoordinator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 19 imports  
**Lines**: 318  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SelfImprovementCoordinator.

## Classes (1)

### `SelfImprovementCoordinator`

Monitors improvements.md, roadmap.txt, context.txt, and prompt.txt.
Automates the monitoring and implementation of improvements and healing.

**Methods** (2):
- `__init__(self, workspace_root)`
- `_init_discovery(self)`

## Dependencies

**Imports** (19):
- `asyncio`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.infrastructure.cloud.budget.BudgetManager`
- `src.infrastructure.mcp_tools.registry.MCPServerRegistry`
- `src.infrastructure.network.LANDiscovery.LANDiscovery`
- `src.infrastructure.orchestration.healing.SelfHealingOrchestrator.SelfHealingOrchestrator`
- `src.infrastructure.orchestration.swarm.DirectorAgent.DirectorAgent`
- `src.logic.agents.intelligence.ResearchAgent.ResearchAgent`
- `traceback`
- `typing.Any`
- ... and 4 more

---
*Auto-generated documentation*
