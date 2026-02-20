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


"""
Auto-extracted class from agent_backend.py
"""

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .provider_type import ProviderType
except ImportError:
    from .provider_type import ProviderType


__version__ = VERSION


@dataclass
class SystemConfig:
    """Configuration for a single backend.
    Attributes:
        name: Backend identifier.
        backend_type: Type of backend.
        enabled: Whether backend is active.
        weight: Weight for load balancing.
        timeout_s: Request timeout in seconds.
        max_retries: Maximum retry attempts.
        rate_limit_rpm: Requests per minute limit.
    """
    name: str
    backend_type: ProviderType
    enabled: bool = True
    weight: int = 1
    timeout_s: int = 60
    max_retries: int = 2
    rate_limit_rpm: int | None = None
