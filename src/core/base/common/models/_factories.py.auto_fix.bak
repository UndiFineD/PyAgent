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
# See the License for the specific language governing permissions and
# limitations under the License.


"""Factory functions for dataclass default fields.
Isolated from model definitions to prevent circularity during analysis.
"""

try:
    from typing import TYPE_CHECKING, Any, Callable
except ImportError:
    from typing import TYPE_CHECKING, Any, Callable


if TYPE_CHECKING:
    from .base_models import ConfigProfile, ModelConfig
    from .core_enums import AgentEvent, FilePriority


def _empty_agent_event_handlers() -> dict[AgentEvent, list[Callable[..., None]]]:
    """Factory for agent event handlers."""
    return {}


def _empty_dict_str_configprofile() -> dict[str, ConfigProfile]:
    """Factory for ConfigProfile dict."""
    return {}


def _empty_dict_str_filepriority() -> dict[str, FilePriority]:
    """Factory for FilePriority dict."""
    return {}


def _empty_dict_str_modelconfig() -> dict[str, ModelConfig]:
    """Factory for ModelConfig dict."""
    return {}


def _empty_routes_list() -> list[tuple[Callable[[Any], bool], Callable[[Any], Any]]]:
    """Factory for routes list."""
    return []


def _empty_list_str() -> list[str]:
    """Factory for empty list of strings."""
    return []


def _empty_list_int() -> list[int]:
    """Factory for empty list of integers."""
    return []


def _empty_list_float() -> list[float]:
    """Factory for empty list of floats."""
    return []


def _empty_list_dict_str_any() -> list[dict[str, Any]]:
    """Factory for empty list of dicts."""
    return []


def _empty_dict_str_any() -> dict[str, Any]:
    """Factory for empty dict."""
    return {}


def _empty_dict_str_str() -> dict[str, str]:
    """Factory for empty dict of strings."""
    return {}


def _empty_dict_str_int() -> dict[str, int]:
    """Factory for empty dict of integers."""
    return {}


def _empty_dict_str_float() -> dict[str, float]:
    """Factory for empty dict of floats."""
    return {}


def _empty_dict_str_callable_any_any() -> dict[str, Callable[[Any], Any]]:
    """Factory for empty dict of callables."""
    return {}


def _empty_dict_str_health_checks() -> dict[str, Callable[[], dict[str, Any]]]:
    """Factory for empty health checks dict."""
    return {}


def _empty_dict_str_quality_criteria() -> dict[str, tuple[Callable[[str], float], float]]:
    """Factory for quality criteria."""
    return {}
