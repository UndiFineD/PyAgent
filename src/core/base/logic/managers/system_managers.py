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

"""
System Managers for PyAgent.
(Facade for src.core.base.common.*_core)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from src.core.base.common.models import AgentEvent, _empty_agent_event_handlers


@dataclass
class EventManager:
    """Manages agent events. (Facade)"""

    handlers: dict[AgentEvent, list[Callable[..., None]]] = field(default_factory=_empty_agent_event_handlers)

    def on(self, event: AgentEvent, handler: Callable[..., None]) -> None:
        """Register an event handler."""
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def emit(self, event: AgentEvent, data: Any = None) -> None:
        """Emit an event to all registered handlers."""
        if event in self.handlers:
            for handler in self.handlers[event]:
                if data is not None:
                    handler(data)
                else:
                    handler()


@dataclass
class StatePersistence:
    """Persists agent state. (Facade)"""

    state_file: Any
    backup: bool = False
    backup_count: int = 0

    def save(self, state: dict[str, Any]) -> None:
        """Save the agent state."""

    def load(self, default: dict[str, Any] | None = None) -> dict[str, Any]:
        """Load the agent state."""
        return default or {}


@dataclass
class FilePriorityManager:
    """Manages file priorities. (Facade)"""

    def __init__(self, config: Any = None):
        from src.core.base.common.priority_core import PriorityCore
        self._core = PriorityCore(config)

    def get_priority(self, path: Path) -> Any:
        """Get priority for a path."""
        return self._core.get_priority(path)


@dataclass
class HealthChecker:
    """Checks system health. (Facade)"""

    def __init__(self, workspace_root: Path | None = None):
        from src.core.base.common.health_core import HealthCore
        self._core = HealthCore(workspace_root)

    def check_git(self) -> Any:
        """Check git status."""
        return self._core.check_git()


@dataclass
class ProfileManager:
    """Manages execution profiles. (Facade)"""

    def __init__(self):
        from src.core.base.common.profile_core import ProfileCore
        self._core = ProfileCore()

    def activate(self, name: str) -> None:
        """Activate a profile."""
        self._core.activate(name)


@dataclass
class ResponseCache:
    """Caches responses. (Facade)"""

    def __init__(self, cache_dir: Path | None = None):
        from src.core.base.common.cache_core import CacheCore
        self._core = CacheCore(cache_dir)

    def get(self, key: str) -> Any:
        """Get cached response."""
        return self._core.get(key)
