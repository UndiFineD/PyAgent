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
SLA Level - Define SLA priority enumeration

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import and use the SLALevel enum to represent ticket/issue priority and map to target response windows:
  from src.core.base.sla_level import SLALevel
  deadline = sla_mapping[SLALevel.P0]

WHAT IT DOES:
- Provides a small, explicit Enum (SLALevel) enumerating SLA priority levels P0..P4 with integer values and inline human-readable comments indicating typical target windows (24 hours → 1 month).

WHAT IT SHOULD DO BETTER:
- Attach explicit metadata (timedeltas or ISO durations) to each member instead of relying on comments, provide helper methods to compute deadlines, add serialization/deserialization (to/from JSON and strings), and include unit tests and documentation linking these levels to SLAs used across the system.
- Consider making the module location and import path consistent with package layout and adding type hints and a module-level docstring explaining intended semantics.

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


class SLALevel(Enum):
    """SLA priority levels."""

    P0 = 1  # 24 hours
    P1 = 2  # 3 days
    P2 = 3  # 1 week
    P3 = 4  # 2 weeks
    P4 = 5  # 1 month
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SLALevel(Enum):
    """SLA priority levels."""

    P0 = 1  # 24 hours
    P1 = 2  # 3 days
    P2 = 3  # 1 week
    P3 = 4  # 2 weeks
    P4 = 5  # 1 month
