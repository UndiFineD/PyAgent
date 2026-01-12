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



































@dataclass(init=False)
class ImprovementTemplate:
    """Template for creating improvements.

    Compatibility notes:
    - Tests construct templates without `id`/`category`.
    - Tests sometimes pass `description_pattern` instead of `description_template`.
    - `instantiate()` returns a dict with `title` and `description`.
    """

    id: str
    name: str
    category: ImprovementCategory
    title_pattern: str
    description_template: str
    default_priority: ImprovementPriority
    default_effort: EffortEstimate

    def __init__(
        self,
        id: str = "",
        name: str = "",
        category: ImprovementCategory = ImprovementCategory.OTHER,
        title_pattern: str = "",
        description_template: str = "",
        description_pattern: str = "",
        default_priority: ImprovementPriority = ImprovementPriority.MEDIUM,
        default_effort: EffortEstimate = EffortEstimate.MEDIUM,
        **_: Any,
    ) -> None:
        if not description_template and description_pattern:
            description_template = description_pattern

        resolved_id = (id or name or "template").strip()
        resolved_name = (name or resolved_id).strip()

        self.id = resolved_id
        self.name = resolved_name
        self.category = category
        self.title_pattern = title_pattern
        self.description_template = description_template
        self.default_priority = default_priority
        self.default_effort = default_effort

    def instantiate(self, variables: Dict[str, str]) -> Dict[str, str]:
        """Instantiate the template with variables."""
        return {
            "title": self.title_pattern.format(**variables),
            "description": self.description_template.format(**variables),
        }
