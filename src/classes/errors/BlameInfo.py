#!/usr/bin/env python3

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging
import re
import subprocess

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
