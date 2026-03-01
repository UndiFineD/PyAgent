# self_evolution_mixin

**File**: `src\logic\agents\swarm\self_evolution_mixin.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 370  
**Complexity**: 13 (moderate)

## Overview

Self-evolution mixin for PyAgent orchestrators.

## Classes (3)

### `EvolutionMetrics`

Metrics for tracking workflow performance.

### `EvolutionHistory`

History of workflow evolution attempts.

### `SelfEvolutionMixin`

Mixin that enables self-evolving capabilities for PyAgent orchestrators.

This mixin implements automatic workflow optimization based on execution
feedback, inspired by EvoAgentX's self-evolution algorithms.

**Methods** (13):
- `__init__(self)`
- `enable_evolution(self, enabled)`
- `set_evolution_params(self, max_iterations, improvement_threshold)`
- `_calculate_metrics(self, result)`
- `_should_evolve(self, metrics)`
- `_analyze_workflow_issues(self, result, metrics)`
- `_apply_evolution_suggestions(self, current_result, suggestions, iteration)`
- `_is_improved(self, old_metrics, new_metrics)`
- `_record_evolution_step(self, workflow_id, result, metrics)`
- `_extract_lessons(self, result, metrics)`
- ... and 3 more methods

## Dependencies

**Imports** (13):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.common.models.communication_models.WorkState`
- `src.core.base.work_patterns.WorkPattern`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
