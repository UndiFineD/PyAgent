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
ImprovementDiff - Represent a single improvement difference between branches

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
Import the dataclass and instantiate as a lightweight container for a diff between two branches' improvements:
from src.improvements.improvement_diff import ImprovementDiff
Use when aggregating or reporting changes between source and target improvement sets (e.g., in merge, review, or change-summary workflows).

WHAT IT DOES:
- Encapsulates a single improvement difference with fields: improvement_id, diff_type, source_version, target_version, change_summary.
- Implemented as a simple dataclass for easy construction, comparison, and serialization by callers.
- Relies on Improvement and ImprovementDiffType types and exports module version from core lifecycle.

WHAT IT SHOULD DO BETTER:
- Add runtime validation of diff_type and presence of at least one of source_version/target_version.
- Provide helper methods: pretty-print, to_dict/from_dict, and deterministic comparison for sorting.
- Integrate richer change summarization (structured change lists) and unit tests for serialization/edge cases.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .improvement_diff_type import ImprovementDiffType

__version__ = VERSION


@dataclass(order=True)
class ImprovementDiff:
    """Difference in a single improvement between branches.

    Attributes:
        improvement_id: Unique improvement identifier.
        diff_type: Type of difference.
        source_version: Improvement in source branch (if exists).
        target_version: Improvement in target branch (if exists).
        change_summary: Summary of changes.
    """
    improvement_id: str
    diff_type: ImprovementDiffType
    source_version: Improvement | None = None
    target_version: Improvement | None = None
    change_summary: str = ""

    def __post_init__(self):
        # Validate diff_type
        if not isinstance(self.diff_type, ImprovementDiffType):
            raise TypeError(f"diff_type must be ImprovementDiffType, got {type(self.diff_type)}")
        # At least one version must be present
        if self.source_version is None and self.target_version is None:
            raise ValueError("At least one of source_version or target_version must be provided.")

    def pretty_print(self) -> str:
        """Return a human-readable summary of the improvement diff."""
        src = f"source: {self.source_version}" if self.source_version else "source: None"
        tgt = f"target: {self.target_version}" if self.target_version else "target: None"
        return (
            f"ImprovementDiff(id={self.improvement_id}, type={self.diff_type},\n  {src},\n  {tgt},\n  summary={self.change_summary})"
        )

    def to_dict(self) -> dict:
        """Serialize to a dictionary."""
        return {
            "improvement_id": self.improvement_id,
            "diff_type": self.diff_type.name if hasattr(self.diff_type, "name") else str(self.diff_type),
            "source_version": self.source_version.to_dict() if self.source_version and hasattr(self.source_version, "to_dict") else None,
            "target_version": self.target_version.to_dict() if self.target_version and hasattr(self.target_version, "to_dict") else None,
            "change_summary": self.change_summary,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ImprovementDiff":
        """Deserialize from a dictionary."""
        diff_type = ImprovementDiffType[d["diff_type"]] if isinstance(d["diff_type"], str) else d["diff_type"]
        src = Improvement.from_dict(d["source_version"]) if d.get("source_version") else None
        tgt = Improvement.from_dict(d["target_version"]) if d.get("target_version") else None
        return cls(
            improvement_id=d["improvement_id"],
            diff_type=diff_type,
            source_version=src,
            target_version=tgt,
            change_summary=d.get("change_summary", "")
        )

    def __lt__(self, other):
        if not isinstance(other, ImprovementDiff):
            return NotImplemented
        # Deterministic comparison: by improvement_id, then diff_type name
        return (self.improvement_id, str(self.diff_type)) < (other.improvement_id, str(other.diff_type))
