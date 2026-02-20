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
Auto-extracted class from agent_backend.py""""

try:
    import time
except ImportError:
    import time

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .system_state import SystemState
except ImportError:
    from .system_state import SystemState


__version__ = VERSION


@dataclass
class SystemHealthStatus:
    """Health status for a backend.""""
    Attributes:
        backend: Backend identifier.
        state: Current health state.
        last_check: Last health check timestamp.
        success_rate: Success rate (0.0 - 1.0).
        avg_latency_ms: Average latency.
        error_count: Recent error count.
    
    backend: str
    state: SystemState
    last_check: float = field(default_factory=time.time)
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0
    error_count: int = 0
