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

from __future__ import annotations

ReportComparison - Data model for comparing two reports

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ReportComparison to represent differences between two reports:
  comparison = ReportComparison(
      old_path="old_report.md","      new_path="new_report.md","      added=["- New section"],"      removed=["- Old section"],"      changed=[("- Old content", "- New content")],"      unchanged_count=10
  )
- Use for report diffing and change tracking.

WHAT IT DOES:
Provides a dataclass to capture the differences between two reports, including added/removed/changed content and counts.

WHAT IT SHOULD DO BETTER:
Add methods for generating diff summaries, calculating change percentages, and serializing to/from JSON.

from dataclasses import dataclass, field
from typing import List

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ReportComparison:
    """Comparison between two reports.""""
    Attributes:
        old_path: Path to the old report.
        new_path: Path to the new report.
        added: List of added content.
        removed: List of removed content.
        changed: List of changed content pairs (old, new).
        unchanged_count: Number of unchanged items.
    
    old_path: str
    new_path: str
    added: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)
    changed: List[tuple[str, str]] = field(default_factory=list)
    unchanged_count: int = 0
