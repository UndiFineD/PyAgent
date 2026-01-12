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



from .EffortEstimate import EffortEstimate
from .ImprovementCategory import ImprovementCategory
from .ImprovementPriority import ImprovementPriority
from .ImprovementStatus import ImprovementStatus

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
class Improvement:
    """A single improvement suggestion."""
    id: str
    title: str
    description: str
    file_path: str
    priority: ImprovementPriority = ImprovementPriority.MEDIUM
    category: ImprovementCategory = ImprovementCategory.OTHER
    status: ImprovementStatus = ImprovementStatus.PROPOSED
    effort: EffortEstimate = EffortEstimate.MEDIUM
    impact_score: float = 50.0
    created_at: str = ""
    updated_at: str = ""
    assignee: Optional[str] = None
    tags: List[str] = field(default_factory=list)  # type: ignore[assignment]
    dependencies: List[str] = field(default_factory=list)  # type: ignore[assignment]
    votes: int = 0
