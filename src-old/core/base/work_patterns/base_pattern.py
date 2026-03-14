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

## Source: src-old/core/base/work_patterns/base_pattern.description.md

# base_pattern

**File**: `src\\core\base\\work_patterns\base_pattern.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 62  
**Complexity**: 3 (simple)

## Overview

Base Work Pattern for PyAgent swarm collaboration patterns.

## Classes (1)

### `WorkPattern`

**Inherits from**: ABC

Abstract base class for work patterns in PyAgent swarm.

Work patterns define how multiple agents collaborate on tasks,
inspired by agentUniverse PEER pattern and other collaborative frameworks.

**Methods** (3):
- `__init__(self, name, description)`
- `validate_agents(self)`
- `get_required_agents(self)`

## Dependencies

**Imports** (6):
- `abc.ABC`
- `abc.abstractmethod`
- `src.core.base.common.models.communication_models.CascadeContext`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/work_patterns/base_pattern.improvements.md

# Improvements for base_pattern

**File**: `src\\core\base\\work_patterns\base_pattern.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `base_pattern_test.py` with pytest tests

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

r"""Base Work Pattern for PyAgent swarm collaboration patterns."""
