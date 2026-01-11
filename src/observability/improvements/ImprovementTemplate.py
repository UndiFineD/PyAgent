#!/usr/bin/env python3
from __future__ import annotations
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


































from src.core.base.version import VERSION
__version__ = VERSION

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
