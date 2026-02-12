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
report_comparison.py - ReportComparison dataclass for report diffs

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate to hold the difference between two report versions:
  from report_comparison import ReportComparison
  comp = ReportComparison(old_path="reports/v1.json", new_path="reports/v2.json")
  # populate comp.added, comp.removed, comp.changed, comp.unchanged_count as produced by a diff routine
- Used as a simple data container returned by generate_agent_reports.py or similar report-diffing utilities.
- Suitable for serialization (e.g., to JSON) or simple presentation layers.

WHAT IT DOES:
- Provides a compact, typed dataclass to convey the result of comparing two report files: paths for old/new, lists of added and removed items, a list of changed item tuples, and a count of unchanged items.
- Serves as a plain data carrier with default empty collections for ease of incremental population by diffing code.

WHAT IT SHOULD DO BETTER:
- Use pathlib.Path (Path) for old_path/new_path instead of plain str for clearer path handling and cross-platform correctness.
- Make changed tuple types explicit (e.g., list[tuple[str, str]] or a small dataclass) so consumers know the shape of each change entry.
- Add convenience methods: .to_dict(), .from_dict(), __bool__ or .is_empty(), and validation in __post_init__ to enforce invariants.
- Consider immutability (frozen dataclass) or read-only accessors when used as an immutable diff result; provide tests for serialization and equality semantics.
- Document expected contents of added/removed/changed (e.g., identifiers vs full objects) and include examples in the module docstring.

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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ReportComparison:
    """Result of comparing two report versions.
    Attributes:
        old_path: Path to old version.
        new_path: Path to new version.
        added: Items added in new version.
        removed: Items removed from old version.
        changed: Items that changed (list of tuples of old, new).
        unchanged_count: Count of unchanged items.
    """

    old_path: str
    new_path: str
    added: list[str] = field(default_factory=list)  # type: ignore[assignment]
    removed: list[str] = field(default_factory=list)  # type: ignore[assignment]
    changed: list[tuple] = field(default_factory=list)  # type: ignore[assignment]
    unchanged_count: int = 0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ReportComparison:
    """Result of comparing two report versions.
    Attributes:
        old_path: Path to old version.
        new_path: Path to new version.
        added: Items added in new version.
        removed: Items removed from old version.
        changed: Items that changed (list of tuples of old, new).
        unchanged_count: Count of unchanged items.
    """

    old_path: str
    new_path: str
    added: list[str] = field(default_factory=list)  # type: ignore[assignment]
    removed: list[str] = field(default_factory=list)  # type: ignore[assignment]
    changed: list[tuple] = field(default_factory=list)  # type: ignore[assignment]
    unchanged_count: int = 0
