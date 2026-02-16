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

"""
Improvement - Dataclass for representing a single improvement suggestion

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
from improvement import Improvement, ImprovementPriority, ImprovementCategory, ImprovementStatus, EffortEstimate
imp = Improvement(
    id="IMP-0001",
    title="Reduce cyclomatic complexity in parser.py",
    description="Refactor long functions into smaller units and add unit tests.",
    file_path="src/parser.py",
    priority=ImprovementPriority.HIGH,
    category=ImprovementCategory.REFACTOR,
    status=ImprovementStatus.PROPOSED,
    effort=EffortEstimate.MEDIUM,
    impact_score=75.0,
    created_at="2026-02-12T12:00:00Z"
)

WHAT IT DOES:
- Provides a plain dataclass model named Improvement that captures metadata for a suggested code change or improvement.
- Fields include identifiers, human-readable title/description, file path, priority, category, status, effort estimate, impact_score, timestamps, assignee, tags, dependencies and vote count.
- Uses enums and small helper types (ImprovementPriority, ImprovementCategory, ImprovementStatus, EffortEstimate) for structured values and imports a repository VERSION into __version__.

WHAT IT SHOULD DO BETTER:
- Validate and normalize fields (ensure ISO8601 datetimes, non-empty id/title, sane impact_score range) and convert created_at/updated_at to timezone-aware datetime objects instead of strings.
- Provide serialization (to_dict/from_dict), equality/hash semantics, and helper methods for state transitions (propose/accept/complete) and vote management to centralize business rules.
- Integrate with transactional FS (StateTransaction) and CascadeContext for safe persistent updates, and add unit tests for edge cases (missing fields, invalid enums, large dependency graphs).

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .effort_estimate import EffortEstimate
from .improvement_category import ImprovementCategory
from .improvement_priority import ImprovementPriority
from .improvement_status import ImprovementStatus

__version__ = VERSION


@dataclass
class Improvement:
    """A single improvement suggestion."""

    id: str
    title: str
    description: str
    file_path: str
    priority: ImprovementPriority = ImprovementPriority.MEDIUM
    category: ImprovementCategory = ImprovementCategory.OTHER
    status: ImprovementStatus = ImprovementStatus.PROPOSED
    effort: EffortEstimate = EffortEstimate.MEDIUM
    impact_score: float = 50.0
    created_at: str = ""
    updated_at: str = ""
    assignee: str | None = None
    tags: list[str] = field(default_factory=list)  # type: ignore[assignment]
    dependencies: list[str] = field(default_factory=list)  # type: ignore[assignment]
    votes: int = 0
