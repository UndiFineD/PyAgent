#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .AnalysisToolType import AnalysisToolType

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
class ToolSuggestion:
    """Suggestion from a code analysis tool.

    Attributes:
        tool_type: Type of analysis tool.
        tool_name: Name of the specific tool.
        file_path: File with the issue.
        line_number: Line number of the issue.
        message: Suggestion message.
        suggested_fix: Optional code fix.
    """
    tool_type: AnalysisToolType
    tool_name: str
    file_path: str
    line_number: int
    message: str
    suggested_fix: str = ""
