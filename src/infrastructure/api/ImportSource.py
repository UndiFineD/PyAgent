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

class ImportSource(Enum):
    """External sources for changelog import."""
    GITHUB_RELEASES = "github_releases"
    JIRA = "jira"
    GITLAB = "gitlab"
    MANUAL = "manual"
