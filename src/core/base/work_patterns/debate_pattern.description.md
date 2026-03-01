# debate_pattern

**File**: `src\core\base\work_patterns\debate_pattern.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 9 imports  
**Lines**: 394  
**Complexity**: 4 (simple)

## Overview

Debate work pattern implementation for multi-agent adversarial reasoning.

## Classes (3)

### `DebateAgent`

Represents an agent in a debate with specific role and incentives.

### `DebateConfig`

Configuration for debate pattern execution.

### `DebateWorkPattern`

**Inherits from**: WorkPattern

Implements opponent processor / multi-agent debate pattern.

This pattern spawns opposing agents with different goals or perspectives
to debate solutions, reducing bias and improving decision quality through
adversarial reasoning.

**Methods** (4):
- `__init__(self, name, description, advocate_agent, auditor_agent)`
- `validate_agents(self, agents)`
- `_find_agent_by_id(self, agent_id)`
- `_check_consensus(self, round_results)`

## Dependencies

**Imports** (9):
- `asyncio`
- `dataclasses.dataclass`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.common.models.communication_models.WorkState`
- `src.core.base.work_patterns.base_pattern.WorkPattern`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
