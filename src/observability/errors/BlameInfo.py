#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_errors.py"""

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class BlameInfo:
    """Git blame information for an error.

    Attributes:
        error_id: ID of the error.
        commit_hash: Commit that introduced the error.
        author: Author of the commit.
        commit_date: Date of the commit.
        commit_message: Commit message.
    """
    error_id: str
    commit_hash: str = ""
    author: str = ""
    commit_date: str = ""
    commit_message: str = ""
