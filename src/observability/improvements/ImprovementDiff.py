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

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .Improvement import Improvement
from .ImprovementDiffType import ImprovementDiffType
from dataclasses import dataclass
from typing import Optional

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