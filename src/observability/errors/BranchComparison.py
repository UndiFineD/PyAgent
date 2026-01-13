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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass, field
from typing import List

__version__ = VERSION

@dataclass
class BranchComparison:
    """Comparison of errors across branches.

    Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        errors_only_in_a: Error IDs only in branch A.
        errors_only_in_b: Error IDs only in branch B.
        common_errors: Error IDs in both branches.
    """
    branch_a: str
    branch_b: str
    errors_only_in_a: list[str] = field(default_factory=lambda: [])
    errors_only_in_b: list[str] = field(default_factory=lambda: [])
    common_errors: list[str] = field(default_factory=lambda: [])