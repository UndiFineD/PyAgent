#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/models/agent_models.description.md

# agent_models

**File**: `src\\core\base\\models\agent_models.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 14 imports  
**Lines**: 127  
**Complexity**: 7 (moderate)

## Overview

Models for agent configuration, state, and plugins.

## Classes (8)

### `AgentConfig`

Agent configuration from environment or file.

### `ComposedAgent`

Configuration for agent composition.

### `AgentHealthCheck`

Health check result for an agent.

### `AgentPluginConfig`

Configuration for an agent plugin.

### `ExecutionProfile`

A profile for agent execution settings.

### `AgentPipeline`

Chains agent steps sequentially.

**Methods** (2):
- `add_step(self, name, func)`
- `execute(self, data)`

### `AgentParallel`

Executes agent branches in parallel conceptually.

**Methods** (2):
- `add_branch(self, name, func)`
- `execute(self, data)`

### `AgentRouter`

Routes input based on conditions.

**Methods** (3):
- `add_route(self, condition, handler)`
- `set_default(self, handler)`
- `route(self, data)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base_models._empty_dict_str_any`
- `base_models._empty_dict_str_callable_any_any`
- `base_models._empty_list_str`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.AgentPriority`
- `enums.HealthStatus`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/models/agent_models.improvements.md

# Improvements for agent_models

**File**: `src\\core\base\\models\agent_models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 127 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `agent_models_test.py` with pytest tests

### Code Organization
- [TIP] **8 classes in one file** - Consider splitting into separate modules

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
from __future__ import annotations


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

r"""Models for agent configuration, state, and plugins."""
