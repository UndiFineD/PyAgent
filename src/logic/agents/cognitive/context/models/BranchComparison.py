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


"""Auto-extracted class from agent_context.py"""




from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import hashlib
import json
import logging
import re
import zlib

@dataclass
class BranchComparison:
    """Comparison of context across branches.

    Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        files_only_in_a: Files only in branch A.
        files_only_in_b: Files only in branch B.
        modified_files: Files modified between branches.
    """
    branch_a: str
    branch_b: str
    files_only_in_a: List[str] = field(default_factory=lambda: [])
    files_only_in_b: List[str] = field(default_factory=lambda: [])
    modified_files: List[str] = field(default_factory=lambda: [])
