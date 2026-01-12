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


"""Auto-extracted class from generate_agent_reports.py"""



from .CodeIssue import CodeIssue

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time



































@dataclass
class AggregatedReport:
    """Report aggregated from multiple sources.
    Attributes:
        sources: Source report paths.
        combined_issues: Combined issues from all sources.
        summary: Aggregation summary.
        generated_at: Generation timestamp.
    """

    sources: List[str] = field(default_factory=list)  # type: ignore[assignment]
    combined_issues: List[CodeIssue] = field(default_factory=list)  # type: ignore[assignment]
    summary: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
    generated_at: float = field(default_factory=time.time)  # type: ignore[assignment]
