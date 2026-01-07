#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class VersioningStrategy(Enum):
    """Supported versioning strategies."""
    SEMVER = "semver"  # Semantic Versioning (MAJOR.MINOR.PATCH)
    CALVER = "calver"  # Calendar Versioning (YYYY.MM.DD)
    CUSTOM = "custom"  # Custom versioning pattern
