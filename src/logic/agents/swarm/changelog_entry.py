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
Changelog Entry - Dataclass representing a single fleet changelog item

Brief Summary
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate to represent changelog lines across the fleet:
  from changelog_entry import ChangelogEntry
  entry = ChangelogEntry(
      category="fix",
      description="Resolve agent deadlock on Windows",
      version="1.4.2",
      date="2026-02-13",
      priority=1,
      severity="high",
      tags=["windows","concurrency"],
      linked_issues=["GH-1234"]
  )
- Use as a lightweight, serializable record in changelog generators, release notes, or audits.

WHAT IT DOES:
- Provides a minimal, explicit dataclass container for changelog metadata: category, description, version, date, priority, severity, tags, and linked issues.
- Keeps structure simple and dependency-free so it can be used across services, scripts, and small tools without heavy runtime requirements.
- Fits into pipelines that collect, filter, and render changelog entries (e.g., convert to markdown, JSON, or populate a release notes template).

WHAT IT SHOULD DO BETTER:
- Replace plain string date with datetime.date (or pydantic model) and validate formats to avoid inconsistent date representations.
- Convert category/severity/priority to enums or constrained types to enforce valid values and simplify filtering/sorting.
- Add serialization helpers (to_dict/from_dict, JSON) and a stable comparison/ordering implementation (by priority/date/version) for deterministic rendering.
- Add input validation (non-empty description, semantic version checks), richer linking to issue objects (not just strings), and unit tests covering serialization and ordering.
- Consider immutability (frozen dataclass) for safety in concurrent contexts and optional methods for human-friendly rendering (short_summary, markdown_line).

FILE CONTENT SUMMARY:
Changelog entry.py module.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ChangelogEntry:
    """Represents a single entry in the fleet-wide changelog."""
    category: str
    description: str
    version: str
    date: str
    priority: int
    severity: str
    tags: List[str] = field(default_factory=list)
    linked_issues: List[str] = field(default_factory=list)
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ChangelogEntry:
    """Represents a single entry in the fleet-wide changelog."""
    category: str
    description: str
    version: str
    date: str
    priority: int
    severity: str
    tags: List[str] = field(default_factory=list)
    linked_issues: List[str] = field(default_factory=list)
