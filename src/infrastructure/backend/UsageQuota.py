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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from dataclasses import dataclass, field
import time

__version__ = VERSION


@dataclass
class UsageQuota:
    """Usage quota configuration.

    Attributes:
        daily_limit: Maximum requests per day.
        hourly_limit: Maximum requests per hour.
        current_daily: Current daily usage.
        current_hourly: Current hourly usage.
        reset_daily_at: When daily count resets.
        reset_hourly_at: When hourly count resets.
    """

    daily_limit: int = 1000
    hourly_limit: int = 100
    current_daily: int = 0
    current_hourly: int = 0
    reset_daily_at: float = field(default_factory=time.time)
    reset_hourly_at: float = field(default_factory=time.time)
