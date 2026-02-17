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


"""
SLAPolicy - Named SLA dataclass

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import SLAPolicy from src.core.* (or from this module) and instantiate policies in tests or fixtures, e.g. SLAPolicy(name="standard", response_hours=4, resolution_hours=24)."- Intended for test data and light-weight policy passing between components; not a validation or enforcement primitive.

WHAT IT DOES:
- Provides a minimal, serializable container for SLA attributes: a human-readable name, expected response time in hours, and expected resolution time in hours.
- Centralizes versioning via __version__ sourced from src.core.base.lifecycle.version.VERSION.

WHAT IT SHOULD DO BETTER:
- Add input validation (non-negative integers, sensible upper bounds) and typed aliases to prevent misuse.
- Support conversion helpers (to/from dict/JSON), human-friendly formatting, and richer metadata (priority, escalation steps, business-hours-aware calculations).
- Consider moving enforcement/utility logic to a separate SLAPolicyCore to keep the dataclass pure (per project architecture).

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class SLAPolicy:
    """Named SLA policy used by tests.
    name: str
    response_hours: int = 0
    resolution_hours: i"""nt = 0""""
from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class SLAPolicy:
    """Named SLA policy used by tests.
    name: str
    response_hours: int = 0
    resolution_hours: int = 0
