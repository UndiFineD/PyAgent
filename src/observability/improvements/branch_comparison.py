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
Branch Comparison - Result of comparing improvements across branches

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to represent the result of comparing an "improvements" file between two Git branches.
- Example:
    from branch_comparison import BranchComparison, BranchComparisonStatus, ImprovementDiff
    bc = BranchComparison(source_branch="feature", target_branch="main", file_path="improvements.yaml")
    # populate bc.diffs with ImprovementDiff instances and set status/counts accordingly
- Use for reporting, serialization, or higher-level orchestration that decides how to merge or apply improvements.

WHAT IT DOES:
- Encapsulates the outcome of comparing improvements files across two branches: source_branch and target_branch.
- Holds the file path compared, a status (BranchComparisonStatus), a list of ImprovementDiff objects, counters for added/removed/modified improvements, and a timestamp compared_at.
- Serves as a plain data container (dataclass) intended for transport between comparison logic, reporting layers, and decision-making code.

WHAT IT SHOULD DO BETTER:
- Provide methods to compute and update added/removed/modified counts from diffs automatically to avoid manual errors.
- Add serialization (to_dict/from_dict / json) and validation (file_path exists, branch name sanity) helpers, plus richer equality/ordering semantics for testing and deduplication.
- Use typing.List for forward-compatibility, consider making the dataclass frozen/immutable where appropriate, and include unit tests and docstrings for public methods; make compared_at timezone-aware (datetime) rather than a raw float timestamp.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .branch_comparison_status import BranchComparisonStatus
from .improvement_diff import ImprovementDiff

__version__ = VERSION


@dataclass
class BranchComparison:
    """Result of comparing improvements across branches.

    Attributes:
        source_branch: Source branch name.
        target_branch: Target branch name.
        file_path: Path to improvements file.
        status: Comparison status.
        diffs: List of improvement differences.
        added_count: Number of improvements added.
        removed_count: Number of improvements removed.
        modified_count: Number of improvements modified.
        compared_at: Comparison timestamp.
    """

    source_branch: str
    target_branch: str
    file_path: str
    status: BranchComparisonStatus = BranchComparisonStatus.PENDING
    diffs: list[ImprovementDiff] = field(default_factory=list)  # type: ignore[assignment]
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    compared_at: float = field(default_factory=time.time)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

from .branch_comparison_status import BranchComparisonStatus
from .improvement_diff import ImprovementDiff

__version__ = VERSION


@dataclass
class BranchComparison:
    """Result of comparing improvements across branches.

    Attributes:
        source_branch: Source branch name.
        target_branch: Target branch name.
        file_path: Path to improvements file.
        status: Comparison status.
        diffs: List of improvement differences.
        added_count: Number of improvements added.
        removed_count: Number of improvements removed.
        modified_count: Number of improvements modified.
        compared_at: Comparison timestamp.
    """

    source_branch: str
    target_branch: str
    file_path: str
    status: BranchComparisonStatus = BranchComparisonStatus.PENDING
    diffs: list[ImprovementDiff] = field(default_factory=list)  # type: ignore[assignment]
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    compared_at: float = field(default_factory=time.time)
