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

## Source: src-old/logic/agents/swarm/agentic_patterns.description.md

# agentic_patterns

**File**: `src\\logic\agents\\swarm\agentic_patterns.py`  
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
## Source: src-old/logic/agents/swarm/agentic_patterns.improvements.md

# Improvements for agentic_patterns

**File**: `src\\logic\agents\\swarm\agentic_patterns.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 382 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `agentic_patterns_test.py` with pytest tests

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

r"""Sequential agent orchestration pattern."""
