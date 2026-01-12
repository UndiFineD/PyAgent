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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Helper functions for dataclass default factories."""




from typing import Any, Final, TypeVar, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.base.models import AgentPluginConfig

# Import optional dependencies
try:
    import requests as _requests
except ImportError:  # pragma: no cover
    _requests = None

requests = _requests
HAS_REQUESTS: Final[bool] = _requests is not None

try:
    from tqdm import tqdm as _tqdm
except ImportError:  # pragma: no cover
    _tqdm = None

HAS_TQDM: Final[bool] = _tqdm is not None

_T = TypeVar("_T")

if _tqdm is not None:
    tqdm = _tqdm
else:

    def tqdm(iterable: Iterable[_T], *args: Any, **kwargs: Any) -> Iterable[_T]:
        """Fallback if tqdm not available."""
        return iterable


def _empty_dict_str_any() -> dict[str, Any]:
    """Helper function for default factory in dataclass fields."""
    return {}


def _empty_dict_str_float() -> dict[str, float]:
    """Helper function for default factory in dataclass fields."""
    return {}


def _empty_dict_str_int() -> dict[str, int]:
    """Helper function for default factory in dataclass fields."""
    return {}


def _empty_dict_str_str() -> dict[str, str]:
    """Helper function for default factory in dataclass fields."""
    return {}


def _empty_list_str() -> list[str]:
    """Helper function for default factory in dataclass fields."""
    return []


def _empty_list_dict_str_any() -> list[dict[str, Any]]:
    """Helper function for default factory in dataclass fields."""
    return []


def _empty_plugin_config_list() -> list[AgentPluginConfig]:
    """Helper function for default factory in dataclass fields."""
    # Import here to avoid circular dependency
    from src.core.base.models import AgentPluginConfig
    return []
