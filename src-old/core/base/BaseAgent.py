#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/BaseAgent.description.md

# BaseAgent

**File**: `src\\core\base\\BaseAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 26 imports  
**Lines**: 292  
**Complexity**: 13 (moderate)

## Overview

BaseAgent main class and core agent logic.

## Classes (1)

### `BaseAgent`

**Inherits from**: IdentityMixin, PersistenceMixin, KnowledgeMixin, OrchestrationMixin, GovernanceMixin

Core AI Agent Shell (Synaptic modularization Phase 317).
Inherits domain logic from specialized Mixins to maintain low complexity.

**Methods** (13):
- `register_plugin(cls, name_or_plugin, plugin)`
- `unregister_plugin(cls, name)`
- `get_plugin(cls, name)`
- `__init__(self, file_path)`
- `_run_command(self, cmd, timeout)`
- `run(self, prompt)`
- `_notify_webhooks(self, event, data)`
- `get_model(self)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- ... and 3 more methods

## Dependencies

**Imports** (26):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `logging`
- `pathlib.Path`
- `requests`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.BaseAgentCore.BaseAgentCore`
- `src.core.base.ShellExecutor.ShellExecutor`
- `src.core.base.Version.VERSION`
- `src.core.base.mixins.GovernanceMixin.GovernanceMixin`
- `src.core.base.mixins.IdentityMixin.IdentityMixin`
- `src.core.base.mixins.KnowledgeMixin.KnowledgeMixin`
- `src.core.base.mixins.OrchestrationMixin.OrchestrationMixin`
- `src.core.base.mixins.PersistenceMixin.PersistenceMixin`
- ... and 11 more

---
*Auto-generated documentation*
## Source: src-old/core/base/BaseAgent.improvements.md

# Improvements for BaseAgent

**File**: `src\\core\base\\BaseAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 292 lines (medium)  
**Complexity**: 13 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BaseAgent_test.py` with pytest tests

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

r"""BaseAgent main class and core agent logic."""
