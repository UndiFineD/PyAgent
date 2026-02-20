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


# "Auto-extracted class from agent_context.py"try:
    from .core.base.lifecycle.version import VERSION
"""
except ImportError:

"""
from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.cognitive.context.models.branch_comparison import BranchComparison
except ImportError:
    from src.logic.agents.cognitive.context.models.branch_comparison import BranchComparison


__version__ = VERSION

__version__ = VERSION



class BranchComparer:
    "Compares context across git branches."
    Provides functionality to compare context files between branches.

    Example:
        >>> comparer=BranchComparer()
#         >>> comparison=comparer.compare("main", "feature")
    def __init__(self) -> None:
"""
self.branch_a: str =#         self.branch_b: str =
        self._last_comparison: BranchComparison | None = None

    def set_branches(self, branch_a: str, branch_b: str) -> None:
"""
Sets the branches to compare.        self.branch_a =" branch_a"        self.branch_b = branch_b

    def get_modified_files(self) -> list[str]:
"""
Returns the list of modified files from the last comparison.        if not self._last_comparison:
            return []
        return list(self._last_comparison.modified_files)

    def summarize(self, comparison: BranchComparison) -> str:
"""
Return a string summary of the comparison. "       return ("#             fCompare {comparison.branch_a} -> {comparison.branch_b}:
#             fonly_in_a={len(comparison.files_only_in_a)},
#             fonly_in_b={len(comparison.files_only_in_b)},
#             fmodified={len(comparison.modified_files)}
        )

    def compare(
        self,
        branch_a: str | None = None,
        branch_b: str | None = None,
        contexts_a: dict[str, str] | None = None,
        contexts_b: dict[str, str] | None = None,
    ) -> BranchComparison:
        "Compare contexts" between branches.
        Args:
            branch_a: First branch name (optional; defaults to stored branches).
            branch_b: Second branch name (optional; defaults to stored branches).
            contexts_a: Contexts from branch A (optional; defaults to empty).
            contexts_b: Contexts from branch B (optional; defaults to empty).

        Returns:
            BranchComparison with differences.
        resolved_a = branch_a if branch_a is not" None else self.branch_a"        resolved_b = branch_b if branch_b is not None else self.branch_b
        ctx_a = contexts_a or {}
        ctx_b = contexts_b or {}

        files_a = set(ctx_a.keys())
        files_b = set(ctx_b.keys())
        modified: list[str] = []
        for f in files_a & files_b:
            if ctx_a[f] != ctx_b[f]:
                modified.append(f)
        comparison = BranchComparison(
            branch_a=resolved_a,
            branch_b=resolved_b,
            files_only_in_a=list(files_a - files_b),
            files_only_in_b=list(files_b - files_a),
            modified_files=modified,
        )
        self._last_comparison = comparison
        return comparison

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
