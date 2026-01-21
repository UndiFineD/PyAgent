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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .schedule_status import ScheduleStatus
from dataclasses import dataclass, field

__version__ = VERSION


@dataclass
class ScheduledImprovement:
    """A scheduled improvement with resource allocation.

    Attributes:
        improvement_id: ID of the scheduled improvement.
        scheduled_start: Planned start date.
        scheduled_end: Planned end date.
        assigned_resources: List of assigned team members.
        status: Current schedule status.
        sprint_id: Optional sprint identifier.
    """

    improvement_id: str
    scheduled_start: str = ""
    scheduled_end: str = ""
    assigned_resources: list[str] = field(default_factory=list)  # type: ignore[assignment]
    status: ScheduleStatus = ScheduleStatus.UNSCHEDULED
    sprint_id: str = ""
