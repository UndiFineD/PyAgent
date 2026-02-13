#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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


"""
schedule_status.py - ScheduleStatus enum for scheduled improvements

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the enum and use it to represent or check the scheduling state of an improvement or task:
  from src.core.base.schedule_status import ScheduleStatus
  status = ScheduleStatus.SCHEDULED
  if status is ScheduleStatus.OVERDUE: handle_overdue()
- Use in dataclasses, persistence layers, and APIs as a canonical set of possible schedule states.

WHAT IT DOES:
Defines a compact, single-purpose Enum (ScheduleStatus) capturing the lifecycle states used by the agent improvement scheduling subsystem: UNSCHEDULED, SCHEDULED, IN_SPRINT, BLOCKED, and OVERDUE; exposes __version__ from the lifecycle version module for module versioning.

WHAT IT SHOULD DO BETTER:
- Provide richer metadata per status (human-friendly labels, severity, workflow transitions) and helper methods (e.g., is_active(), is_blocking(), to_serializable())
- Add explicit tests exercising equality, serialization/deserialization, and integration with persistence layers (JSON, DB enum)
- Include module-level docstring describing placement in the architecture and an importable constant mapping for UI/display and i18n

FILE CONTENT SUMMARY:
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

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ScheduleStatus(Enum):
    """Status of scheduled improvements."""

    UNSCHEDULED = "unscheduled"
    SCHEDULED = "scheduled"
    IN_SPRINT = "in_sprint"
    BLOCKED = "blocked"
    OVERDUE = "overdue"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ScheduleStatus(Enum):
    """Status of scheduled improvements."""

    UNSCHEDULED = "unscheduled"
    SCHEDULED = "scheduled"
    IN_SPRINT = "in_sprint"
    BLOCKED = "blocked"
    OVERDUE = "overdue"
