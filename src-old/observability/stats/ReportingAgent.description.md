# ReportingAgent

**File**: `src\observability\stats\ReportingAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 22 imports  
**Lines**: 115  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for ReportingAgent.

## Classes (1)

### `ReportingAgent`

**Inherits from**: BaseAgent

Observer agent that generates executive dashboards and reports
by orchestrating multiple specialist agents.

**Methods** (1):
- `__init__(self, fleet)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `asyncio`
- `datetime.datetime`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `src.logic.agents.cognitive.MemoryConsolidationAgent.MemoryConsolidationAgent`
- `src.logic.agents.cognitive.VisualizerAgent.VisualizerAgent`
- `src.logic.agents.development.PullRequestAgent.PRAgent`
- `src.logic.agents.development.SpecToolAgent.SpecToolAgent`
- `src.logic.agents.development.TestAgent.TestAgent`
- `src.logic.agents.development.ToolEvolutionAgent.ToolEvolutionAgent`
- `src.logic.agents.intelligence.BrowsingAgent.BrowsingAgent`
- ... and 7 more

---
*Auto-generated documentation*
