#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/managers/SystemManagers.description.md

# SystemManagers

**File**: `src\core\base\managers\SystemManagers.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 28 imports  
**Lines**: 348  
**Complexity**: 33 (complex)

## Overview

Python module containing implementation for SystemManagers.

## Classes (6)

### `FilePriorityManager`

Manager for file priority and request ordering.

**Methods** (6):
- `__init__(self, config)`
- `set_pattern_priority(self, pattern, priority)`
- `set_extension_priority(self, extension, priority)`
- `get_priority(self, path)`
- `sort_by_priority(self, paths)`
- `filter_by_priority(self, paths, min_priority)`

### `ResponseCache`

Caches responses based on prompts. 
Supports Prompt Caching (Phase 128) by identifying prefix reusable contexts.

**Methods** (5):
- `__post_init__(self)`
- `_get_cache_key(self, prompt)`
- `set(self, prompt, response)`
- `get(self, prompt)`
- `invalidate(self, prompt)`

### `StatePersistence`

Persists agent state to disk.

**Methods** (2):
- `save(self, state)`
- `load(self, default)`

### `EventManager`

Manages agent events.

**Methods** (2):
- `on(self, event, handler)`
- `emit(self, event, data)`

### `HealthChecker`

Performs health checks on agent components.

**Methods** (10):
- `__init__(self, repo_root, recorder)`
- `add_check(self, name, check_func)`
- `record_request(self, success, latency_ms)`
- `get_metrics(self)`
- `check(self)`
- `check_agent_script(self, agent_name)`
- `check_git(self)`
- `check_python(self)`
- `run_all_checks(self)`
- `is_healthy(self)`

### `ProfileManager`

Manages configuration profiles and execution profiles.

**Methods** (8):
- `__init__(self)`
- `_register_defaults(self)`
- `add_profile(self, profile)`
- `activate(self, name)`
- `set_active(self, name)`
- `get_active_config(self)`
- `active(self)`
- `get_setting(self, key, default)`

## Dependencies

**Imports** (28):
- `__future__.annotations`
- `ast`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `fnmatch`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.models.AgentEvent`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.ConfigProfile`
- `src.core.base.models.ExecutionProfile`
- `src.core.base.models.FilePriority`
- ... and 13 more

---
*Auto-generated documentation*
## Source: src-old/core/base/managers/SystemManagers.improvements.md

# Improvements for SystemManagers

**File**: `src\core\base\managers\SystemManagers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 348 lines (medium)  
**Complexity**: 33 score (complex)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SystemManagers_test.py` with pytest tests

### Code Organization
- [TIP] **6 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

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

# Optional import for PluginManager

from src.core.base.version import VERSION
import hashlib
import json
import logging
import sys
import time
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections.abc import Callable
from src.core.base.models import (
    FilePriority,
    FilePriorityConfig,
    AgentEvent,
    ConfigProfile,
    HealthStatus,
    AgentHealthCheck,
    ExecutionProfile,
    _empty_dict_str_str,
    _empty_agent_event_handlers,
)

try:
    from src.infrastructure.fleet.VersionGate import VersionGate
except ImportError:
    VersionGate = None

__version__ = VERSION

# Phase 108: Multi-Agent Logic Harvesting.
# Intelligence operations are recorded via record_interaction in Agent classes.


class FilePriorityManager:
    """Manager for file priority and request ordering."""

    def __init__(self, config: FilePriorityConfig | None = None) -> None:
        self.config = config or FilePriorityConfig()
        self._default_extensions = {
            ".py": FilePriority.HIGH,
            ".js": FilePriority.HIGH,
            ".ts": FilePriority.HIGH,
            ".md": FilePriority.NORMAL,
            ".json": FilePriority.LOW,
            ".txt": FilePriority.LOW,
        }

    def set_pattern_priority(self, pattern: str, priority: FilePriority) -> None:
        self.config.path_patterns[pattern] = priority

    def set_extension_priority(self, extension: str, priority: FilePriority) -> None:
        self.config.extension_priorities[extension] = priority

    def get_priority(self, path: Path) -> FilePriority:
        import fnmatch

        path_str = str(path)
        for pattern, priority in self.config.path_patterns.items():
            if fnmatch.fnmatch(path_str, pattern):
                return priority
        ext = path.suffix.lower()
        if ext in self.config.extension_priorities:
            return self.config.extension_priorities[ext]
        if ext in self._default_extensions:
            return self._default_extensions[ext]
        return self.config.default_priority

    def sort_by_priority(self, paths: list[Path]) -> list[Path]:
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)

    def filter_by_priority(
        self, paths: list[Path], min_priority: FilePriority = FilePriority.LOW
    ) -> list[Path]:
        return [p for p in paths if self.get_priority(p).value >= min_priority.value]


@dataclass
class ResponseCache:
    """
    Caches responses based on prompts.
    Supports Prompt Caching (Phase 128) by identifying prefix reusable contexts.
    """

    cache_dir: Path
    cache_data: dict[str, str] = field(default_factory=_empty_dict_str_str)
    prefix_map: dict[str, str] = field(default_factory=_empty_dict_str_str)

    def __post_init__(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode()).hexdigest()

    def set(self, prompt: str, response: str) -> None:
        key = self._get_cache_key(prompt)
        self.cache_data[key] = response

        # Support prefix caching: Index the first 500 chars (approx. context window prefix)
        if len(prompt) > 500:
            prefix_key = hashlib.md5(prompt[:500].encode()).hexdigest()
            self.prefix_map[prefix_key] = key

        (self.cache_dir / f"{key}.json").write_text(
            json.dumps(
                {"prompt": prompt, "response": response, "timestamp": "2026-01-11"}
            )
        )

    def get(self, prompt: str) -> str | None:
        key = self._get_cache_key(prompt)
        if key in self.cache_data:
            return self.cache_data[key]

        # Check prefix map for partial hits (simulation of provider-side prompt caching)
        if len(prompt) > 500:
            prefix_key = hashlib.md5(prompt[:500].encode()).hexdigest()
            if prefix_key in self.prefix_map:
                logging.info(
                    "ResponseCache: Prompt Prefix hit - internal cache redirection triggered."
                )
                # We still want the full key for safety, but this flags reuse potential

        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            self.cache_data[key] = data["response"]
            return data["response"]
        return None

    def invalidate(self, prompt: str) -> None:
        key = self._get_cache_key(prompt)
        self.cache_data.pop(key, None)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()


@dataclass
class StatePersistence:
    """Persists agent state to disk."""

    state_file: Path
    backup: bool = False
    backup_count: int = 0

    def save(self, state: dict[str, Any]) -> None:
        if self.backup and self.state_file.exists():
            self.state_file.rename(
                self.state_file.parent
                / f"{self.state_file.stem}.{self.backup_count}.bak"
            )
            self.backup_count += 1
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state))

    def load(self, default: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return default or {}


@dataclass
class EventManager:
    """Manages agent events."""

    handlers: dict[AgentEvent, list[Callable[..., None]]] = field(
        default_factory=_empty_agent_event_handlers
    )

    def on(self, event: AgentEvent, handler: Callable[..., None]) -> None:
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def emit(self, event: AgentEvent, data: Any = None) -> None:
        if event in self.handlers:
            for handler in self.handlers[event]:
                if data is not None:
                    handler(data)
                else:
                    handler()


class HealthChecker:
    """Performs health checks on agent components."""

    def __init__(
        self, repo_root: Path | str | None = None, recorder: Any = None
    ) -> None:
        self.repo_root = Path(repo_root) if repo_root else Path.cwd()
        self.recorder = recorder
        self.results: dict[str, AgentHealthCheck] = {}
        # Stub compatibility
        self.checks: dict[str, Callable[[], dict[str, Any]]] = {}
        self.request_count: int = 0
        self.error_count: int = 0
        self.total_latency: int = 0

    def add_check(self, name: str, check_func: Callable[[], dict[str, Any]]) -> None:
        """Stub compatibility."""
        self.checks[name] = check_func

    def record_request(self, success: bool, latency_ms: int) -> None:
        """Stub compatibility."""
        self.request_count += 1
        self.total_latency += latency_ms
        if not success:
            self.error_count += 1

    def get_metrics(self) -> dict[str, Any]:
        """Stub compatibility."""
        error_rate = (
            self.error_count / self.request_count if self.request_count > 0 else 0
        )
        avg_latency = (
            self.total_latency / self.request_count if self.request_count > 0 else 0
        )
        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "avg_latency_ms": avg_latency,
        }

    def check(self) -> dict[str, Any]:
        """Stub compatibility mixed with real check if results exist."""
        components = {name: func() for name, func in self.checks.items()}
        base_status = {"status": "healthy", "components": components}
        if self.results:
            base_status["details"] = {k: v.status.name for k, v in self.results.items()}
        return base_status

    def check_agent_script(self, agent_name: str) -> AgentHealthCheck:
        """Check if an agent script exists and is valid."""
        start_time = time.time()
        # Look for script in src/ directory
        script_path = self.repo_root / f"src/agent_{agent_name}.py"

        if not script_path.exists():
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Script not found: {script_path}",
            )

        try:
            import ast

            content = script_path.read_text(encoding="utf-8", errors="ignore")
            ast.parse(content)
            response_time = (time.time() - start_time) * 1000
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.HEALTHY,
                response_time_ms=response_time,
                details={"script_path": str(script_path)},
            )
        except SyntaxError as e:
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Syntax error: {e}",
            )

    def check_git(self) -> AgentHealthCheck:
        """Check if git is available."""
        start_time = time.time()
        try:
            result = subprocess.run(
                ["git", "--version"], capture_output=True, text=True, timeout=5
            )
            response_time = (time.time() - start_time) * 1000
            if result.returncode == 0:
                return AgentHealthCheck(
                    agent_name="git",
                    status=HealthStatus.HEALTHY,
                    response_time_ms=response_time,
                    details={"version": result.stdout.strip()},
                )
            return AgentHealthCheck(
                agent_name="git",
                status=HealthStatus.UNHEALTHY,
                error_message=result.stderr,
            )
        except Exception as e:
            return AgentHealthCheck(
                agent_name="git", status=HealthStatus.UNHEALTHY, error_message=str(e)
            )

    def check_python(self) -> AgentHealthCheck:
        """Check Python environment."""
        start_time = time.time()
        return AgentHealthCheck(
            agent_name="python",
            status=HealthStatus.HEALTHY,
            response_time_ms=(time.time() - start_time) * 1000,
            details={"version": sys.version, "executable": sys.executable},
        )

    def run_all_checks(self) -> dict[str, AgentHealthCheck]:
        """Run all health checks."""
        agent_names = [
            "coder",
            "tests",
            "changes",
            "context",
            "errors",
            "improvements",
            "stats",
        ]
        self.results["python"] = self.check_python()
        self.results["git"] = self.check_git()
        for name in agent_names:
            self.results[name] = self.check_agent_script(name)
        return self.results

    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        if not self.results:
            self.run_all_checks()
        return all(r.status == HealthStatus.HEALTHY for r in self.results.values())


class ProfileManager:
    """Manages configuration profiles and execution profiles."""

    def __init__(self) -> None:
        self._profiles: dict[str, ExecutionProfile] = {}
        self.profiles: dict[str, ConfigProfile] = {}  # Stub compatibility
        self._active: str | None = None
        self.active_name: str | None = None  # Stub compatibility
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default execution profiles."""
        self._profiles["default"] = ExecutionProfile(
            name="default",
            timeout=120,
            parallel=False,
        )

        self._profiles["fast"] = ExecutionProfile(
            name="fast",
            max_files=10,
            timeout=60,
            parallel=True,
            workers=4,
        )

        self._profiles["ci"] = ExecutionProfile(
            name="ci",
            timeout=300,
            parallel=True,
            workers=2,
            dry_run=True,
        )

    def add_profile(self, profile: Any) -> None:
        """Add a profile (either ExecutionProfile or ConfigProfile)."""
        if hasattr(profile, "name"):
            if isinstance(profile, ExecutionProfile):
                self._profiles[profile.name] = profile
            else:
                self.profiles[profile.name] = profile

    def activate(self, name: str) -> None:
        """Activate a profile by name."""
        if name in self._profiles:
            self._active = name
        if name in self.profiles:
            self.active_name = name

    def set_active(self, name: str) -> None:
        """Stub compatibility."""
        self.activate(name)

    def get_active_config(self) -> ExecutionProfile | None:
        """Get active execution profile."""
        if self._active:
            return self._profiles[self._active]
        return None

    @property
    def active(self) -> Any | None:
        """Get active profile (ConfigProfile takes priority for stub compatibility)."""
        if self.active_name and self.active_name in self.profiles:
            return self.profiles[self.active_name]
        return self.get_active_config()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Stub compatibility for ConfigProfile settings."""
        active_p = self.active
        if not active_p or not hasattr(active_p, "settings"):
            return default

        if key in active_p.settings:
            return active_p.settings[key]

        if (
            hasattr(active_p, "parent")
            and active_p.parent
            and active_p.parent in self.profiles
        ):
            parent = self.profiles[active_p.parent]
            if key in parent.settings:
                return parent.settings[key]
        return default
