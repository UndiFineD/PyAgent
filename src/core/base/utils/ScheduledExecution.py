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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.utils.Helpers import _empty_dict_str_any
from dataclasses import dataclass, field
from typing import Any

__version__ = VERSION


@dataclass
class ScheduledExecution:
    """A scheduled agent execution.

    Attributes:
        name: Schedule name.
        cron: Cron expression (simplified).
        agent_config: Agent configuration.
        enabled: Whether schedule is enabled.
        last_run: Last run timestamp.
        next_run: Next run timestamp.
    """

    name: str
    cron: str  # Simplified: "hourly", "daily", "weekly", or HH:MM
    agent_config: dict[str, Any] = field(default_factory=_empty_dict_str_any)
    enabled: bool = True
    last_run: float | None = None
    next_run: float | None = None
