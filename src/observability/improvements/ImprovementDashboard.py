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



from .Improvement import Improvement

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



































class ImprovementDashboard:
    """Renders a lightweight dashboard and emits update callbacks."""

    def __init__(self) -> None:
        self._callbacks: List[Callable[[], None]] = []
        self._improvements: List[Improvement] = []

    def on_update(self, callback: Callable[[], None]) -> None:
        self._callbacks.append(callback)

    def add_improvement(self, improvement: Improvement) -> None:
        self._improvements.append(improvement)
        for cb in list(self._callbacks):
            cb()

    def render(self, improvements: List[Improvement]) -> str:
        lines = ["# Improvements Dashboard"]
        for imp in improvements:
            lines.append(f"- {imp.title}")
        return "\n".join(lines)
