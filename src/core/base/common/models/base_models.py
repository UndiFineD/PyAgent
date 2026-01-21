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

"""Base model classes and utility functions."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from collections.abc import Callable
from .core_enums import AuthMethod, SerializationFormat, FilePriority, AgentEvent

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


def _empty_dict_str_quality_criteria() -> dict[
    str, tuple[Callable[[str], float], float]
]:
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
