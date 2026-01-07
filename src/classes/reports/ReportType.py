#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

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

class ReportType(Enum):
    """Type of report to generate."""

    DESCRIPTION = "description"
    ERRORS = "errors"
    IMPROVEMENTS = "improvements"
    SUMMARY = "summary"
