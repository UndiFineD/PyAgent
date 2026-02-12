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

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .improvement_diff_type import ImprovementDiffType

__version__ = VERSION


@dataclass
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
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement
from .improvement_diff_type import ImprovementDiffType

__version__ = VERSION


@dataclass
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
