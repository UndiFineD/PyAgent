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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_improvements.py"""



from .BranchComparisonStatus import BranchComparisonStatus
from .ImprovementDiff import ImprovementDiff

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time



































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
    diffs: List[ImprovementDiff] = field(default_factory=list)  # type: ignore[assignment]
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    compared_at: float = field(default_factory=time.time)
