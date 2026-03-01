# agentic_patterns

**File**: `src\logic\agents\swarm\agentic_patterns.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 12 imports  
**Lines**: 382  
**Complexity**: 4 (simple)

## Overview

Sequential agent orchestration pattern.

## Classes (3)

### `SequentialAgentConfig`

Configuration for sequential agent execution.

### `SequentialAgentPattern`

Sequential agent execution pattern.

This pattern executes agents in sequence, where each agent's output
can be used as input for subsequent agents. Inspired by agentic design
patterns from ADK (Agentic Design Patterns).

**Methods** (2):
- `__init__(self, orchestrator)`
- `_prepare_next_input(self, current_input, agent_result, agent_config)`

### `ParallelAgentPattern`

Parallel agent execution pattern.

This pattern executes multiple agents concurrently and combines their results.
Inspired by agentic design patterns from ADK.

**Methods** (2):
- `__init__(self, orchestrator)`
- `_combine_parallel_results(self, results)`

## Dependencies

**Imports** (12):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.common.models.communication_models.WorkState`
- `src.logic.agents.swarm.orchestrator_work_pattern_mixin.OrchestratorWorkPatternMixin`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
