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
Scheduled Entry - Compatibility dataclass for scheduled improvements# DATE: 2026-02-12# AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate for tests: from scheduled_entry import ScheduledEntry
- Example: ScheduledEntry(improvement_id="IMP-123", start_date=datetime.now(), resources=["doc.md", "patch.diff"])"
WHAT IT DOES:
- Defines a minimal dataclass ScheduledEntry used for test compatibility containing improvement_id (str), start_date (datetime) and resources (list[str]).
- Exposes module __version__ from src.core.base.lifecycle.version.VERSION to keep the file versioned with the project.

WHAT IT SHOULD DO BETTER:
- Validate inputs (non-empty improvement_id, start_date timezone-awareness and not in the far past/future, resources elements are strings) and raise clear exceptions on invalid data.
- Provide serialization helpers (to_dict/from_dict), richer representation, and optional immutability (frozen=True) for safer test fixtures.
- Remove the type: ignore by using typing.List or by ensuring runtime Python compatibility, and add unit tests covering edge cases and serialization/round-trip behaviour.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ScheduledEntry:
    """Compatibility scheduled entry used by tests.
    improvement_id: str
    start_date: datetime
    resources: list[str] = field(default_factory=list)  # type: ignore[assignment]
