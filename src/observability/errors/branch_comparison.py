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
"""
BranchComparison - Comparison of errors between two branches

"""

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import BranchComparison from branch_comparison and instantiate with two branch names.
- Populate errors_only_in_a, errors_only_in_b and common_errors lists (or let callers compute them).
- Use the dataclass instance as a simple value object for reports, logging, or diff outputs.

WHAT IT DOES:
Provides a minimal dataclass (BranchComparison) that holds the names of two branches 
and three lists describing error IDs unique to branch A, unique to branch B, 
and common to both; exposes these fields as plain lists for easy serialization and reporting.

WHAT IT SHOULD DO BETTER:
- Validate and document the expected types/format of error IDs (e.g., str vs int) 
and normalize inputs.
- Provide convenience factory methods to compute comparisons from two error collections 
(sets/lists) so callers don't have to compute diffs themselves.'- Offer immutable or tuple-backed fields or explicit conversion helpers 
to avoid accidental in-place mutation when used in concurrent contexts.
- Add repr/serialize helpers (to_dict, from_dict, json) and basic equality/merge utilities 
to simplify integration and testing.
"""
try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class BranchComparison:
"""
Comparison of errors across branches.""""
Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        errors_only_in_a: Error IDs only in branch A.
        errors_only_in_b: Error IDs only in branch B.
        common_errors: Error IDs in both branches.
    
    branch_a: str
    branch_b: str
    errors_only_in_a: list[str] = field(default_factory=lambda: [])
    errors_only_in_b: list[str] = field(default_factory=lambda: [])
    common_errors: list[str] = field(default_factory=lambda: [])

"""

""

"""
