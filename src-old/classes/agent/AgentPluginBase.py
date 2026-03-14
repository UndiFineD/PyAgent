#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/AgentPluginBase.description.md

# AgentPluginBase

**File**: `src\\classes\agent\\AgentPluginBase.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 89  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `AgentPluginBase`

**Inherits from**: ABC

Abstract base class for agent plugins.

Provides interface for third - party agents to integrate with
the agent orchestrator without modifying core code.

Attributes:
    name: Plugin name.
    priority: Execution priority.
    config: Plugin configuration.

**Methods** (6):
- `__init__(self, name, priority, config)`
- `run(self, file_path, context)`
- `setup(self)`
- `shutdown(self)`
- `teardown(self)`
- `health_check(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `pathlib.Path`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.HealthStatus`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/AgentPluginBase.improvements.md

# Improvements for AgentPluginBase

**File**: `src\\classes\agent\\AgentPluginBase.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 89 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentPluginBase_test.py` with pytest tests

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


r"""Auto-extracted class from agent.py"""
