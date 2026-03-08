# OrchestrationManagers

**File**: `src\classes\base_agent\managers\OrchestrationManagers.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 14 imports  
**Lines**: 137  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for OrchestrationManagers.

## Classes (4)

### `AgentComposer`

Composer for multi-agent workflows.

**Methods** (5):
- `__init__(self)`
- `add_agent(self, agent)`
- `_calculate_execution_order(self)`
- `execute(self, file_path, prompt, agent_factory)`
- `get_final_result(self)`

### `ModelSelector`

Selects models for different agent types. Supports GLM-4.7 and DeepSeek V4 (roadmap).

**Methods** (3):
- `__post_init__(self)`
- `select(self, agent_type, token_estimate)`
- `set_model(self, agent_type, config)`

### `QualityScorer`

Scores response quality.

**Methods** (2):
- `add_criterion(self, name, func, weight)`
- `score(self, text)`

### `ABTest`

A/B test for variants.

**Methods** (2):
- `__post_init__(self)`
- `select_variant(self)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `agent.BaseAgent`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `random`
- `src.core.base.models.ComposedAgent`
- `src.core.base.models.ModelConfig`
- `src.core.base.models._empty_list_float`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
