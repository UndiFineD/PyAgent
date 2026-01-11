#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class GroupingStrategy(Enum):
    """Strategies for entry grouping."""
    BY_DATE = "by_date"
    BY_VERSION = "by_version"
    BY_CATEGORY = "by_category"
    BY_AUTHOR = "by_author"
