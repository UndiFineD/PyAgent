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
RollbackPoint - Lightweight snapshot container for agent improvement state

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate RollbackPoint(improvement_id, state) to capture a single atomic snapshot of an agent-improvement state; store instances in a history list, persistent store, or a StateTransaction for later restoration. The created_at timestamp is set automatically and can be used to order rollback points. Suitable for quick in-memory snapshots and simple persistence/serialization.

WHAT IT DOES:
Provides a minimal dataclass representing a rollback point for an "improvement" operation, holding an improvement_id, an arbitrary mapping representing state, and an auto-populated creation timestamp (created_at). Exposes a small, typed container that integrates with the project's VERSION metadata to reflect module versioning. Simple and dependency-light so it is easy to create, persist, and compare rollback points."'
WHAT IT SHOULD DO BETTER:
- Validate and document expected structure of state (e.g., require serializable state or provide hooks for serialization/deserialization).
- Make instances immutable or provide explicit copy semantics to avoid accidental mutation of stored snapshots (e.g., deep-copy state on construction or expose a freeze method).
- Add convenience methods: to_dict()/from_dict() for safe serialization, versioned schema checks, and comparison helpers (diff, apply_to(target)).
- Use timezone-aware datetimes (datetime.now(tz=timezone.utc)) and include explicit type hints for compatibility with static analysis and external tools.
- Consider adding equality/hash behavior and richer metadata (author, description, tags) for better auditability.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from datetime import datetime
except ImportError:
    from datetime import datetime

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
class RollbackPoint:
    """A rollback point capturing the state of an improvement at a specific moment.    improvement_id: str
    state: dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
