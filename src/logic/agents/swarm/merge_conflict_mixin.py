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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Merge conflict mixin.py module.
"""

from __future__ import annotations

from typing import Any


class MergeConflictMixin:
    """Mixin for handling merge conflicts in file content."""

    def detect_merge_conflicts(self, content: str) -> list[dict[str, Any]]:
        """Detect merge conflict markers in the content."""
        conflicts: list[dict[str, Any]] = []
        lines = content.split("\n")
        in_conflict = False
        conflict_start = 0
        ours: list[str] = []
        theirs: list[str] = []
        for i, line in enumerate(lines):
            if line.startswith("<<<<<<<"):
                in_conflict = True
                conflict_start = i
                ours = []
            elif line.startswith("=======") and in_conflict:
                pass  # Separator
            elif line.startswith(">>>>>>>") and in_conflict:
                conflicts.append(
                    {
                        "start_line": conflict_start,
                        "end_line": i,
                        "ours": "\n".join(ours),
                        "theirs": "\n".join(theirs),
                    }
                )
                in_conflict = False
                ours = []
                theirs = []
            elif in_conflict:
                # Optimized conflict parsing
                if (
                    "======="
                    not in content[content.find("<<<<<<<", conflict_start) : content.find(line, conflict_start)]
                ):
                    ours.append(line)
                else:
                    theirs.append(line)
        return conflicts

    def resolve_merge_conflict(self, content: str, resolution: str = "ours") -> str:
        """Resolve merge conflicts in the content."""
        result: list[str] = []
        lines = content.split("\n")
        in_conflict = False
        ours_section = True
        ours: list[str] = []
        theirs: list[str] = []

        for line in lines:
            if line.startswith("<<<<<<<"):
                in_conflict = True
                ours_section = True
                ours = []
                theirs = []
            elif line.startswith("=======") and in_conflict:
                ours_section = False
            elif line.startswith(">>>>>>>") and in_conflict:
                # Apply resolution
                if resolution == "ours":
                    result.extend(ours)
                elif resolution == "theirs":
                    result.extend(theirs)
                else:
                    result.extend(ours)
                    result.extend(theirs)
                in_conflict = False
            elif in_conflict:
                if ours_section:
                    ours.append(line)
                else:
                    theirs.append(line)
            else:
                result.append(line)
        return "\n".join(result)
