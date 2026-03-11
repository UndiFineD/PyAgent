#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/reports/report_comparison.description.md

# Description: src/observability/reports/report_comparison.py

Module overview:
- `ReportComparison` dataclass represents the result of comparing two report versions (added/removed/changed items).

Behavioral notes:
- Lightweight container dataclass used by `ReportComparator`.
## Source: src-old/observability/reports/report_comparison.improvements.md

# Improvements: src/observability/reports/report_comparison.py

Potential improvements:
- Add unit tests for `ReportComparison` construction and equality-like semantics.
- Add helper methods to serialize/deserialize comparisons and to produce summary text.

LLM_CONTEXT_END
"""

from __future__ import annotations

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
