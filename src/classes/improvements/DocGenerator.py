#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .Improvement import Improvement

from base_agent import BaseAgent
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

class DocGenerator:
    """Generates simple documentation text for improvements."""

    def __init__(self) -> None:
        self.templates: Dict[str, str] = {
            "default": "## {title}\n\n{description}\n",
        }

    def generate(self, improvement: Improvement, include_metadata: bool = False) -> str:
        base = self.templates["default"].format(title=improvement.title, description=improvement.description)
        if include_metadata:
            meta = getattr(improvement, "metadata", None)
            if isinstance(meta, dict) and meta:
                base += "\n## Metadata\n"
                meta_dict = cast(Dict[str, Any], meta)
                for k, v in meta_dict.items():
                    base += f"- {k}: {v}\n"
        return base
