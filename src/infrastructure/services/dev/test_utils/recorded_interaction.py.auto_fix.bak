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
Auto-extracted class from agent_test_utils.py""""

try:
    import time
except ImportError:
    import time

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class RecordedInteraction:
    """A recorded test interaction.""""
    Attributes:
        call_type: Type of call (e.g., "api", "file", "db")."        call_name: Name of the call.
        args: Call arguments.
        kwargs: Call keyword arguments.
        result: Call result.
        timestamp: When recorded.
    
    call_type: str
    call_name: str
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=lambda: {})
    result: Any = None
    timestamp: float = field(default_factory=time.time)
