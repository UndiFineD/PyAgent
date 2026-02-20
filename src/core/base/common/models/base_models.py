#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
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


"""Base model classes and utility functions."""

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import time

from .core_enums import (AuthMethod, FilePriority,
                         SerializationFormat, EnvironmentStatus, EnvironmentIsolation)
from ._factories import (
    _empty_agent_event_handlers, _empty_dict_str_any,
    _empty_dict_str_callable_any_any, _empty_dict_str_configprofile,
    _empty_dict_str_filepriority, _empty_dict_str_float,
    _empty_dict_str_health_checks, _empty_dict_str_int,
    _empty_dict_str_modelconfig, _empty_dict_str_quality_criteria,
    _empty_dict_str_str, _empty_list_dict_str_any, _empty_list_float,
    _empty_list_int, _empty_list_str, _empty_routes_list)

__all__ = [
    "CacheEntry",
    "AuthConfig",
    "ConfigProfile",
    "SerializationConfig",
    "FilePriorityConfig",
    "ValidationRule",
    "ExecutionCondition",
    "DiffResult",
    "ModelConfig",
    "EnvironmentConfig",
    "EnvironmentInstance",
    "EventHook",
    "_empty_agent_event_handlers",
    "_empty_dict_str_any",
    "_empty_dict_str_callable_any_any",
    "_empty_dict_str_configprofile",
    "_empty_dict_str_filepriority",
    "_empty_dict_str_float",
    "_empty_dict_str_health_checks",
    "_empty_dict_str_int",
    "_empty_dict_str_modelconfig",
    "_empty_dict_str_quality_criteria",
    "_empty_dict_str_str",
    "_empty_list_dict_str_any",
    "_empty_list_float",
    "_empty_list_int",
    "_empty_list_str",
    "_empty_routes_list",
]

# ========== Utility Functions ==========


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
    path_patterns: dict[str, FilePriority] = field(default_factory=_empty_dict_str_filepriority)
    extension_priorities: dict[str, FilePriority] = field(default_factory=_empty_dict_str_filepriority)
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
    error_message: str = ""  # Alias for backward compatibility

    def __post_init__(self) -> None:
        if not self.pattern and self.file_pattern:
            self.pattern = self.file_pattern
        if not self.file_pattern and self.pattern:
            self.file_pattern = self.pattern
        if not self.message and self.error_message:
            self.message = self.error_message
        if not self.error_message and self.message:
            self.error_message = self.message


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
    file_path: Optional[Path | str] = None
    original_content: str = ""
    modified_content: str = ""
    diff_text: str = ""
    diff_lines: list[str] = field(default_factory=_empty_list_str)
    additions: int = 0
    deletions: int = 0
    changes: int = 0


@dataclass(slots=True)
class EnvironmentConfig:
    """Configuration for agent environments."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    tags: list[str] = field(default_factory=_empty_list_str)
    isolation: EnvironmentIsolation = EnvironmentIsolation.NONE
    cpu_limit: float = 1.0  # CPU cores
    memory_limit: int = 1024  # MB
    disk_limit: int = 10240  # MB
    ttl_seconds: int = 1800  # 30 minutes default
    environment_variables: dict[str, str] = field(default_factory=_empty_dict_str_str)
    dependencies: list[str] = field(default_factory=_empty_list_str)
    build_config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    test_config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    deploy_config: dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass(slots=True)
class EnvironmentInstance:
    """Runtime instance of an environment."""
    id: str
    environment_name: str
    status: EnvironmentStatus = EnvironmentStatus.PENDING
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    cpu_usage: float = 0.0
    memory_usage: int = 0
    disk_usage: int = 0
    process_id: Optional[int] = None
    container_id: Optional[str] = None
    working_directory: Optional[Path] = None
    environment_variables: dict[str, str] = field(default_factory=_empty_dict_str_str)
    metadata: dict[str, Any] = field(default_factory=_empty_dict_str_any)


    def is_expired(self) -> bool:
        """Check if the environment instance has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def update_status(self, new_status: EnvironmentStatus) -> None:
        """Update the instance status and timestamp."""
        self.status = new_status
        self.updated_at = time.time()


EventHook = Callable[[dict[str, Any]], None]
