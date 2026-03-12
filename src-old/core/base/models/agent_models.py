#!/usr/bin/env python3
"""LLM_CONTEXT_START

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

"""Models for agent configuration, state, and plugins."""

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .base_models import (
    _empty_dict_str_any,
    _empty_dict_str_callable_any_any,
    _empty_list_str,
)
from .enums import AgentPriority, HealthStatus


@dataclass(slots=True)
class AgentConfig:
    """Agent configuration from environment or file."""

    backend: str = "auto"
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    retry_count: int = 3
    timeout: int = 60
    cache_enabled: bool = True
    token_budget: int = 100000
    dry_run: bool = False


@dataclass(slots=True)
class ComposedAgent:
    """Configuration for agent composition."""

    agent_type: str
    config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    order: int = 0
    depends_on: list[str] = field(default_factory=_empty_list_str)


@dataclass(slots=True)
class AgentHealthCheck:
    """Health check result for an agent."""

    agent_name: str
    status: HealthStatus
    response_time_ms: float = 0.0
    last_check: float = field(default_factory=time.time)
    error_message: str | None = None
    details: dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass(slots=True)
class AgentPluginConfig:
    """Configuration for an agent plugin."""

    name: str
    module_path: str
    entry_point: str = "run"
    priority: AgentPriority = AgentPriority.NORMAL
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass(slots=True)
class ExecutionProfile:
    """A profile for agent execution settings."""

    name: str
    max_files: int | None = None
    timeout: int = 120
    parallel: bool = False
    workers: int = 4
    dry_run: bool = False


@dataclass(slots=True)
class AgentPipeline:
    """Chains agent steps sequentially."""

    steps: dict[str, Callable[[Any], Any]] = field(
        default_factory=_empty_dict_str_callable_any_any
    )
    step_order: list[str] = field(default_factory=_empty_list_str)

    def add_step(self, name: str, func: Callable[[Any], Any]) -> None:
        self.steps[name] = func
        self.step_order.append(name)

    def execute(self, data: Any) -> Any:
        result = data
        for step_name in self.step_order:
            result = self.steps[step_name](result)
        return result


@dataclass(slots=True)
class AgentParallel:
    """Executes agent branches in parallel conceptually."""

    branches: dict[str, Callable[[Any], Any]] = field(
        default_factory=_empty_dict_str_callable_any_any
    )

    def add_branch(self, name: str, func: Callable[[Any], Any]) -> None:
        self.branches[name] = func

    def execute(self, data: Any) -> dict[str, Any]:
        return {name: func(data) for name, func in self.branches.items()}


@dataclass(slots=True)
class AgentRouter:
    """Routes input based on conditions."""

    default_handler: Callable[[Any], Any] | None = None
    routes: list[tuple[Callable[[Any], bool], Callable[[Any], Any]]] = field(
        default_factory=list
    )

    def add_route(
        self, condition: Callable[[Any], bool], handler: Callable[[Any], Any]
    ) -> None:
        self.routes.append((condition, handler))

    def set_default(self, handler: Callable[[Any], Any]) -> None:
        self.default_handler = handler

    def route(self, data: Any) -> Any:
        for condition, handler in self.routes:
            if condition(data):
                return handler(data)
        if self.default_handler:
            return self.default_handler(data)
        return data
