#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/self_evolution_mixin.description.md

# self_evolution_mixin

**File**: `src\\logic\agents\\swarm\\self_evolution_mixin.py`  
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
## Source: src-old/logic/agents/swarm/self_evolution_mixin.improvements.md

# Improvements for self_evolution_mixin

**File**: `src\\logic\agents\\swarm\\self_evolution_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 370 lines (medium)  
**Complexity**: 13 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `self_evolution_mixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

r"""Self-evolution mixin for PyAgent orchestrators."""
