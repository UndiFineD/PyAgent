# IntelligenceOrchestrator

**File**: `src\infrastructure\orchestration\IntelligenceOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 128  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for IntelligenceOrchestrator.

## Classes (1)

### `IntelligenceOrchestrator`

Swarm Collective Intelligence: Analyzes actions and insights from 
multiple agents to find emerging patterns and synthesize "meta-knowledge".
Optimized for Phase 108 with high-performance local AI (vLLM) integration.

**Methods** (5):
- `__init__(self, fleet_manager)`
- `contribute_insight(self, agent_name, insight, confidence)`
- `synthesize_collective_intelligence(self)`
- `get_intelligence_report(self)`
- `get_actionable_improvement_tasks(self)`

## Dependencies

**Imports** (10):
- `IntelligenceCore.IntelligenceCore`
- `__future__.annotations`
- `logging`
- `requests`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LLMClient.LLMClient`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
