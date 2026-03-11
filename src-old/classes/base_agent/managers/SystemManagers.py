#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers/SystemManagers.description.md

# SystemManagers

**File**: `src\\classes\base_agent\\managers\\SystemManagers.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 22 imports  
**Lines**: 155  
**Complexity**: 26 (complex)

## Overview

Python module containing implementation for SystemManagers.

## Classes (7)

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

### `PluginManager`

Manages agent plugins.

**Methods** (3):
- `register(self, plugin)`
- `activate_all(self)`
- `deactivate(self, name)`

### `HealthChecker`

Checks agent health status.

**Methods** (4):
- `add_check(self, name, check_func)`
- `check(self)`
- `record_request(self, success, latency_ms)`
- `get_metrics(self)`

### `ProfileManager`

Manages configuration profiles.

**Methods** (4):
- `active(self)`
- `add_profile(self, profile)`
- `set_active(self, name)`
- `get_setting(self, key, default)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `fnmatch`
- `hashlib`
- `json`
- `logging`
- `models.AgentEvent`
- `models.ConfigProfile`
- `models.FilePriority`
- `models.FilePriorityConfig`
- `models._empty_agent_event_handlers`
- `models._empty_dict_str_any`
- `models._empty_dict_str_configprofile`
- `models._empty_dict_str_health_checks`
- ... and 7 more

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/managers/SystemManagers.improvements.md

# Improvements for SystemManagers

**File**: `src\\classes\base_agent\\managers\\SystemManagers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 155 lines (medium)  
**Complexity**: 26 score (complex)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SystemManagers_test.py` with pytest tests

### Code Organization
- [TIP] **7 classes in one file** - Consider splitting into separate modules

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

# Copyright (c) 2025 PyAgent contributors
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..models import (
    AgentEvent,
    ConfigProfile,
    FilePriority,
    FilePriorityConfig,
    _empty_agent_event_handlers,
    _empty_dict_str_any,
    _empty_dict_str_configprofile,
    _empty_dict_str_health_checks,
    _empty_dict_str_str,
)


class FilePriorityManager:
    """Manager for file priority and request ordering."""

    def __init__(self, config: Optional[FilePriorityConfig] = None) -> None:
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

    def sort_by_priority(self, paths: List[Path]) -> List[Path]:
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)

    def filter_by_priority(
        self, paths: List[Path], min_priority: FilePriority = FilePriority.LOW
    ) -> List[Path]:
        return [p for p in paths if self.get_priority(p).value >= min_priority.value]


@dataclass
class ResponseCache:
    """Caches responses based on prompts."""

    cache_dir: Path
    cache_data: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def __post_init__(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode()).hexdigest()

    def set(self, prompt: str, response: str) -> None:
        key = self._get_cache_key(prompt)
        self.cache_data[key] = response
        (self.cache_dir / f"{key}.json").write_text(
            json.dumps({"prompt": prompt, "response": response})
        )

    def get(self, prompt: str) -> Optional[str]:
        key = self._get_cache_key(prompt)
        if key in self.cache_data:
            return self.cache_data[key]
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

    def save(self, state: Dict[str, Any]) -> None:
        if self.backup and self.state_file.exists():
            self.state_file.rename(
                self.state_file.parent
                / f"{self.state_file.stem}.{self.backup_count}.bak"
            )
            self.backup_count += 1
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(state))

    def load(self, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return default or {}


@dataclass
class EventManager:
    """Manages agent events."""

    handlers: Dict[AgentEvent, List[Callable[..., None]]] = field(
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


@dataclass
class PluginManager:
    """Manages agent plugins."""

    plugins: Dict[str, Any] = field(default_factory=_empty_dict_str_any)

    def register(self, plugin: Any) -> None:
        self.plugins[plugin.name] = plugin

    def activate_all(self) -> None:
        for plugin in self.plugins.values():
            if hasattr(plugin, "activate"):
                plugin.activate()

    def deactivate(self, name: str) -> None:
        if name in self.plugins:
            plugin = self.plugins[name]
            if hasattr(plugin, "deactivate"):
                plugin.deactivate()


@dataclass
class HealthChecker:
    """Checks agent health status."""

    checks: Dict[str, Callable[[], Dict[str, Any]]] = field(
        default_factory=_empty_dict_str_health_checks
    )
    request_count: int = 0
    error_count: int = 0
    total_latency: int = 0

    def add_check(self, name: str, check_func: Callable[[], Dict[str, Any]]) -> None:
        self.checks[name] = check_func

    def check(self) -> Dict[str, Any]:
        components = {name: func() for name, func in self.checks.items()}
        return {"status": "healthy", "components": components}

    def record_request(self, success: bool, latency_ms: int) -> None:
        self.request_count += 1
        self.total_latency += latency_ms
        if not success:
            self.error_count += 1

    def get_metrics(self) -> Dict[str, Any]:
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


@dataclass
class ProfileManager:
    """Manages configuration profiles."""

    profiles: Dict[str, ConfigProfile] = field(
        default_factory=_empty_dict_str_configprofile
    )
    active_name: Optional[str] = None

    @property
    def active(self) -> Optional[ConfigProfile]:
        return self.profiles.get(self.active_name) if self.active_name else None

    def add_profile(self, profile: ConfigProfile) -> None:
        self.profiles[profile.name] = profile

    def set_active(self, name: str) -> None:
        if name in self.profiles:
            self.active_name = name

    def get_setting(self, key: str, default: Any = None) -> Any:
        if not self.active:
            return default
        if key in self.active.settings:
            return self.active.settings[key]
        if self.active.parent and self.active.parent in self.profiles:
            parent = self.profiles[self.active.parent]
            if key in parent.settings:
                return parent.settings[key]
        return default
