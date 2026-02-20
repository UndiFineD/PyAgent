#!/usr/bin/env python3
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


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

try:
    from src.core.base.common.utils.helpers import _empty_dict_str_any
except Exception:
    def _empty_dict_str_any() -> dict[str, Any]:
        return {}


@dataclass
class ScheduledExecution:
    """A scheduled agent execution.

    Simple dataclass used in tests to represent scheduled runs.
    """

    name: str
    cron: str  # Simplified: "hourly", "daily", "weekly", or HH:MM
    agent_config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    enabled: bool = True
    last_run: float | None = None
    next_run: float | None = None
