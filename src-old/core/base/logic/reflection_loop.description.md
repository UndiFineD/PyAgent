# reflection_loop

**File**: `src\core\base\logic\reflection_loop.py`  
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
