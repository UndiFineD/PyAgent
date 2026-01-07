#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

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

class AnalysisToolType(Enum):
    """Types of code analysis tools."""
    LINTER = "linter"
    TYPE_CHECKER = "type_checker"
    SECURITY_SCANNER = "security_scanner"
    COVERAGE = "coverage"
    COMPLEXITY = "complexity"
