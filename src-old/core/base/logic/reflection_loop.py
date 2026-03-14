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

## Source: src-old/core/base/logic/reflection_loop.description.md

# reflection_loop

**File**: `src\\core\base\\logic\reflection_loop.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 15 imports  
**Lines**: 318  
**Complexity**: 6 (moderate)

## Overview

Reflection Loop System for Self-Improving Agents

This module implements an iterative reflection pattern where agents can:
1. Generate initial solutions/code
2. Reflect on their work through critique
3. Refine based on feedback
4. Repeat until satisfactory results are achieved

Based on patterns from agentic_design_patterns repository.

## Classes (7)

### `ReflectionResult`

**Inherits from**: BaseModel

Result of a reflection iteration.

### `ReflectionLoopConfig`

**Inherits from**: BaseModel

Configuration for reflection loop execution.

### `ReflectionContext`

Context maintained throughout the reflection loop.

### `ReflectionAgent`

**Inherits from**: ABC

Abstract base class for agents that can participate in reflection loops.

### `LLMReflectionAgent`

**Inherits from**: ReflectionAgent

LLM-based reflection agent using any LLM provider.

**Methods** (1):
- `__init__(self, llm_callable, name)`

### `CodeReflectionAgent`

**Inherits from**: LLMReflectionAgent

Specialized agent for code reflection and improvement.

**Methods** (1):
- `__init__(self, llm_callable, language)`

### `ReflectionLoopOrchestrator`

Orchestrates the reflection loop process.

**Methods** (4):
- `__init__(self, generator_agent, critic_agent)`
- `_is_content_perfect(self, critique)`
- `get_final_result(self, context)`
- `get_reflection_summary(self, context)`

## Dependencies

**Imports** (15):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `logging`
- `pydantic.BaseModel`
- `pydantic.Field`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/reflection_loop.improvements.md

# Improvements for reflection_loop

**File**: `src\\core\base\\logic\reflection_loop.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 318 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `reflection_loop_test.py` with pytest tests

### Code Organization
- [TIP] **7 classes in one file** - Consider splitting into separate modules

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

"""
Reflection Loop System for Self-Improving Agents

This module implements an iterative reflection pattern where agents can:
1. Generate initial solutions/code
2. Reflect on their work through critique
3. Refine based on feedback
4. Repeat until satisfactory results are achieved

Based on patterns from agentic_design_patterns repository.
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ReflectionResult(BaseModel):
    """
    """
