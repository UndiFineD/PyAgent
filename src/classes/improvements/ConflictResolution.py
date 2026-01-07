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

@dataclass
class ConflictResolution:
    """Resolution for a conflicting improvement.

    Attributes:
        improvement_id: ID of conflicting improvement.
        resolution: Resolved improvement version.
        strategy: Resolution strategy used.
        resolved_by: Who resolved the conflict.
    """
    improvement_id: str
    resolution: Improvement
    strategy: str = "manual"
    resolved_by: str = ""
