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

class ImprovementExporter:
    """Exports improvements to json/csv."""

    def __init__(self) -> None:
        self.formats: List[str] = ["json", "csv"]

    def export(self, improvements: List[Improvement], format: str = "json") -> str:
        fmt = format.lower()
        if fmt == "json":
            rows: List[Dict[str, Any]] = []
            for imp in improvements:
                rows.append({
                    "id": imp.id,
                    "title": imp.title,
                    "description": imp.description,
                })
            return json.dumps(rows)
        if fmt == "csv":
            lines = ["id,title,description"]
            for imp in improvements:
                lines.append(f"{imp.id},{imp.title},{imp.description}")
            return "\n".join(lines)
        raise ValueError("Unsupported format")
