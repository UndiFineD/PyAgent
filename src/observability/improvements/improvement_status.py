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
Improvement Status - Define ImprovementStatus enum

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the enum and use as canonical states for improvement lifecycle controls and checks.
- Examples:
  - from src.core.base.improvement_status import ImprovementStatus
  - if improvement.status is ImprovementStatus.APPROVED: proceed()
  - str(ImprovementStatus.PROPOSED.value)  # 'proposed'

WHAT IT DOES:
- Provides a small, explicit Enum named ImprovementStatus that centralizes the canonical lifecycle states for agent improvements (proposed, approved, in_progress, completed, rejected, deferred).
- Exposes __version__ tied to the project's VERSION constant for traceability.

WHAT IT SHOULD DO BETTER:
- Add richer docstrings, serialization/deserialization helpers, and string-to-enum lookup utilities for robust external integration (JSON, DB).
- Include unit tests and examples showing canonical usage patterns and migration strategies if states change.
- Consider adding metadata per state (human-readable label, transition rules) or integrating with the project's StateTransaction / lifecycle tooling.

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


class ImprovementStatus(Enum):
    """Status of an improvement."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    DEFERRED = "deferred"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ImprovementStatus(Enum):
    """Status of an improvement."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    DEFERRED = "deferred"
