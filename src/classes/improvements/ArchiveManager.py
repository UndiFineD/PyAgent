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

class ArchiveManager:
    """Archives completed improvements."""

    def __init__(self) -> None:
        self.archived: List[Improvement] = []

    def archive(self, improvement: Improvement) -> None:
        self.archived.append(improvement)

    def restore(self, improvement_id: str) -> Improvement:
        for i, imp in enumerate(list(self.archived)):
            if imp.id == improvement_id:
                self.archived.pop(i)
                return imp
        raise KeyError(improvement_id)
