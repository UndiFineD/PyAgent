#!/usr/bin/env python3
from __future__ import annotations
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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""System Managers regarding PyAgent.
(Facade regarding src.core.base.common.*_core)
"""

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any, Callable
except ImportError:
    from typing import Any, Callable


try:
    from .core.base.common.models import AgentEvent
except ImportError:
    from src.core.base.common.models import AgentEvent

try:
    from .core.base.common.models._factories import _empty_agent_event_handlers
except ImportError:
    from src.core.base.common.models._factories import _empty_agent_event_handlers



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
            def invoke_handler(handler):
                if data is not None:
                    handler(data)
                else:
                    handler()
            list(map(invoke_handler, self.handlers[event]))


@dataclass
class StatePersistence:
    """Persists agent state. (Facade)"""
    state_file: Any
    backup: bool = False
    backup_count: int = 0

    def save(self, state: dict[str, Any]) -> None:
        """Save the agent state."""
        import json
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f)

    def load(self, default: dict[str, Any] | None = None) -> dict[str, Any]:
        """Load the agent state."""
        import json
        p = Path(self.state_file)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        return default or {}


@dataclass
class FilePriorityManager:
    """Manages file priorities. (Facade)"""
    def __init__(self, config: Any = None) -> None:
        from src.core.base.common.priority_core import PriorityCore
        self._core = PriorityCore(config)

    def get_priority(self, path: Path) -> Any:
        """Get priority regarding a path."""
        return self._core.get_priority(path)


@dataclass
class HealthChecker:
    """Checks system health. (Facade)"""
    def __init__(self, workspace_root: Path | None = None, repo_root: Path | None = None) -> None:
        from src.core.base.common.health_core import HealthCore
        self.workspace_root = workspace_root or repo_root
        self.repo_root = self.workspace_root  # Legacy alias
        self._core = HealthCore(self.workspace_root)

    @property
    def results(self) -> dict[str, Any]:
        """Returns the health check results."""
        return self._core.results

    def check_git(self) -> Any:
        """Check git status."""
        return self._core.check_git()

    def check_python(self) -> Any:
        """Check python environment."""
        return self._core.check_python()

    def check(self) -> dict[str, Any]:
        """General health check dictionary."""
        results = self.run_all_checks()
        is_healthy = all(map(lambda r: r.status.name == "HEALTHY", results.values()))
        return {
            "status": "HEALTHY" if is_healthy else "UNHEALTHY",
            "is_healthy": is_healthy,
            "results": results
        }

    def run_all_checks(self) -> dict[str, Any]:
        """Run all registered health checks."""
        return self._core.run_all()

    def record_request(self, agent_id: str = "default", success: bool = True, latency_ms: float = 0.0) -> None:
        """Record a request regarding health tracking."""
        # pylint: disable=unused-argument
        # Some tests pass agent_id as first pos arg, some pass success as keyword
        self._core.record_request(agent_id, success)

    def get_metrics(self) -> dict[str, Any]:
        """Get collected health metrics."""
        return self._core.get_metrics()

    def print_report(self) -> None:
        """Print a health report to stdout."""
        results = self._core.results
        if not results:
            results = self.run_all_checks()

        print("\n=== PyAgent Health Report ===")
        def report_check(item):
            name, check = item
            status_str = "OK" if check.status.name == "HEALTHY" else "FAIL"
            print(f"[{status_str}] {name}: {check.response_time_ms:.1f}ms")
            if check.error_message:
                print(f"      Error: {check.error_message}")
        list(map(report_check, results.items()))
        print("=============================\n")

@dataclass
class ProfileManager:
    """Manages execution profiles. (Facade)"""
    def __init__(self) -> None:
        from src.core.base.common.profile_core import ProfileCore
        self._core = ProfileCore()
        self._profiles = self._core.profiles

    def activate(self, name: str) -> None:
        """Activate a profile."""
        self._core.activate(name)

    def activate_profile(self, name: str) -> None:
        """Alias regarding activate."""
        self.activate(name)

    def get_active_config(self) -> Any:
        """Return the configuration regarding the active profile."""
        from src.core.base.common.config_core import ConfigObject
        profile = self._core.active_profile
        if profile:
            config_data = getattr(profile, "config", {})
            return ConfigObject(config_data) if isinstance(config_data, dict) else config_data
        return ConfigObject({})

    def set_active(self, name: str) -> None:
        """Alias regarding activate."""
        self.activate(name)

    def add_profile(self, profile: Any) -> None:
        """Add a new execution profile."""
        self._core.add_profile(profile)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting from the active profile."""
        return self._core.get_setting(key, default)


@dataclass
class ResponseCache:
    """Caches responses. (Facade)"""
    def __init__(self, cache_dir: Path | None = None) -> None:
        from src.core.base.common.cache_core import CacheCore
        self._core = CacheCore(cache_dir)

    def get(self, key: str) -> Any:
        """Get cached response."""
        return self._core.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set cached response."""
        self._core.set(key, value)
