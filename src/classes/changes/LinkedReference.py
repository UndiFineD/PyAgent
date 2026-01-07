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

@dataclass
class LinkedReference:
    """A linked reference to commit or issue.

    Attributes:
        ref_type: Type of reference ('commit' or 'issue').
        ref_id: ID of the reference.
        url: URL to the reference.
        title: Title / description of the reference.
    """
    ref_type: str
    ref_id: str
    url: str = ""
    title: str = ""
