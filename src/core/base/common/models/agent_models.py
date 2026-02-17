#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Models for agent configuration, state, and plugins."""
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from .base_models import (_empty_dict_str_any,
                          _empty_dict_str_callable_any_any, _empty_list_str)
from .core_enums import AgentPriority, HealthStatus


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
    config: dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass(slots=True)
class AgentPipeline:
    """Chains agent steps sequentially."""
    steps: dict[str, Callable[[Any], Any]] = field(default_factory=_empty_dict_str_callable_any_any)
    step_order: list[str] = field(default_factory=_empty_list_str)

    def add_step(self, name: str, func: Callable[[Any], Any]) -> None:
        """Add an execution step to the pipeline."""
        self.steps[name] = func
        self.step_order.append(name)

    def execute(self, data: Any) -> Any:
        """Execute all steps regarding the pipeline sequentially functionally."""
        from functools import reduce
        return reduce(lambda res, name: self.steps[name](res), self.step_order, data)


@dataclass(slots=True)
class AgentParallel:
    """Executes agent branches in parallel conceptually."""
    branches: dict[str, Callable[[Any], Any]] = field(default_factory=_empty_dict_str_callable_any_any)

    def add_branch(self, name: str, func: Callable[[Any], Any]) -> None:
        """Add a parallel execution branch."""
        self.branches[name] = func

    def execute(self, data: Any) -> dict[str, Any]:
           """Execute all branches regarding parallel results functionally."""
           return dict(map(lambda item: (item[0], item[1](data)), self.branches.items()))


@dataclass(slots=True)
class AgentRouter:
    """Routes input based on conditions."""
    default_handler: Callable[[Any], Any] | None = None
    routes: list[tuple[Callable[[Any], bool], Callable[[Any], Any]]] = field(default_factory=list)

    def add_route(self, condition: Callable[[Any], bool], handler: Callable[[Any], Any]) -> None:
           """Add a conditional route."""
           self.routes.append((condition, handler))

    def set_default(self, handler: Callable[[Any], Any]) -> None:
        """Set the default handler for unmatched routes."""
        self.default_handler = handler

    def route(self, data: Any) -> Any:
        """Route the input data regarding registered conditions functionally."""
        match = next(filter(lambda r: r[0](data), self.routes), None)
        if match:
            return match[1](data)

        if self.default_handler:
            return self.default_handler(data)
        return data
