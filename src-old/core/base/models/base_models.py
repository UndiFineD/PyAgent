#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/models/base_models.description.md

# base_models

**File**: `src\\core\base\\models\base_models.py`  
**Type**: Python Module  
**Summary**: 9 classes, 16 functions, 16 imports  
**Lines**: 174  
**Complexity**: 18 (moderate)

## Overview

Base model classes and utility functions.

## Classes (9)

### `CacheEntry`

Cached response entry.

### `AuthConfig`

Authentication configuration.

### `SerializationConfig`

Configuration for custom serialization.

### `FilePriorityConfig`

Configuration for file priority.

### `ExecutionCondition`

A condition for agent execution.

### `ValidationRule`

Consolidated validation rule for Phase 126.

**Methods** (1):
- `__post_init__(self)`

### `ModelConfig`

Model configuration.

### `ConfigProfile`

Configuration profile.

**Methods** (1):
- `get(self, key, default)`

### `DiffResult`

Result of a diff operation.

## Functions (16)

### `_empty_agent_event_handlers()`

### `_empty_list_str()`

### `_empty_list_int()`

### `_empty_list_float()`

### `_empty_list_dict_str_any()`

### `_empty_dict_str_float()`

### `_empty_dict_str_any()`

### `_empty_dict_str_int()`

### `_empty_dict_str_str()`

### `_empty_dict_str_callable_any_any()`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enums.AgentEvent`
- `enums.AuthMethod`
- `enums.DiffOutputFormat`
- `enums.FilePriority`
- `enums.SerializationFormat`
- `pathlib.Path`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 1 more

---
*Auto-generated documentation*
## Source: src-old/core/base/models/base_models.improvements.md

# Improvements for base_models

**File**: `src\\core\base\\models\base_models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 174 lines (medium)  
**Complexity**: 18 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `base_models_test.py` with pytest tests

### Code Organization
- [TIP] **9 classes in one file** - Consider splitting into separate modules

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

"""Base model classes and utility functions."""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .enums import (
    AgentEvent,
    AuthMethod,
    FilePriority,
    SerializationFormat,
)


# ========== Utility Functions ==========
def _empty_agent_event_handlers() -> dict[AgentEvent, list[Callable[..., None]]]:
    return {}


def _empty_list_str() -> list[str]:
    return []


def _empty_list_int() -> list[int]:
    return []


def _empty_list_float() -> list[float]:
    return []


def _empty_list_dict_str_any() -> list[dict[str, Any]]:
    return []


def _empty_dict_str_float() -> dict[str, float]:
    return {}


def _empty_dict_str_any() -> dict[str, Any]:
    return {}


def _empty_dict_str_int() -> dict[str, int]:
    return {}


def _empty_dict_str_str() -> dict[str, str]:
    return {}


def _empty_dict_str_callable_any_any() -> dict[str, Callable[[Any], Any]]:
    return {}


def _empty_dict_str_quality_criteria() -> (
    dict[str, tuple[Callable[[str], float], float]]
):
    return {}


def _empty_dict_str_health_checks() -> dict[str, Callable[[], dict[str, Any]]]:
    return {}


def _empty_dict_str_configprofile() -> dict[str, ConfigProfile]:
    return {}


def _empty_routes_list() -> list[tuple[Callable[[Any], bool], Callable[[Any], Any]]]:
    return []


def _empty_dict_str_filepriority() -> dict[str, FilePriority]:
    return {}


def _empty_dict_str_modelconfig() -> dict[str, ModelConfig]:
    return {}


# ========== Dataclasses ==========


@dataclass(slots=True)
class CacheEntry:
    """Cached response entry."""

    key: str
    response: str
    timestamp: float
    hit_count: int = 0
    quality_score: float = 0.0


@dataclass(slots=True)
class AuthConfig:
    """Authentication configuration."""

    method: AuthMethod = AuthMethod.NONE
    api_key: str = ""
    token: str = ""
    username: str = ""
    password: str = ""
    oauth_client_id: str = ""
    oauth_client_secret: str = ""
    custom_headers: dict[str, str] = field(default_factory=_empty_dict_str_str)


@dataclass(slots=True)
class SerializationConfig:
    """Configuration for custom serialization."""

    format: SerializationFormat = SerializationFormat.JSON
    options: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    compression: bool = False
    encryption: bool = False


@dataclass(slots=True)
class FilePriorityConfig:
    """Configuration for file priority."""

    path_patterns: dict[str, FilePriority] = field(
        default_factory=_empty_dict_str_filepriority
    )
    extension_priorities: dict[str, FilePriority] = field(
        default_factory=_empty_dict_str_filepriority
    )
    default_priority: FilePriority = FilePriority.NORMAL


@dataclass(slots=True)
class ExecutionCondition:
    """A condition for agent execution."""

    name: str
    check: Callable[[Path, str], bool]
    description: str = ""


@dataclass(slots=True)
class ValidationRule:
    """Consolidated validation rule for Phase 126."""

    name: str
    pattern: str = ""
    message: str = "Validation failed"
    severity: str = "error"  # error, warning, info
    validator: Callable[[str, Path], bool] | None = None
    required: bool = False
    file_pattern: str = ""  # Alias for backward compatibility

    def __post_init__(self) -> None:
        if not self.pattern and self.file_pattern:
            self.pattern = self.file_pattern
        if not self.file_pattern and self.pattern:
            self.file_pattern = self.pattern


@dataclass(slots=True)
class ModelConfig:
    """Model configuration."""

    model_id: str
    temperature: float = 0.7
    max_tokens: int = 2000
    enable_thinking: bool = False
    max_thinking_tokens: int = 2000


@dataclass(slots=True)
class ConfigProfile:
    """Configuration profile."""

    name: str
    settings: dict[str, Any]
    parent: str | None = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        return self.settings.get(key, default)


@dataclass(slots=True)
class DiffResult:
    """Result of a diff operation."""

    file_path: Path
    original_content: str
    modified_content: str
    diff_lines: list[str] = field(default_factory=_empty_list_str)
    additions: int = 0
    deletions: int = 0
    changes: int = 0


EventHook = Callable[[dict[str, Any]], None]
