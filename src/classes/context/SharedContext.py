#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .SharingPermission import SharingPermission

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

@dataclass
class SharedContext:
    """Context shared with team members.

    Attributes:
        context_id: Unique identifier.
        owner: Owner username.
        shared_with: List of usernames shared with.
        permission: Permission level.
        last_sync: Last synchronization timestamp.
    """
    context_id: str
    owner: str
    shared_with: List[str] = field(default_factory=lambda: [])
    permission: SharingPermission = SharingPermission.READ_ONLY
    last_sync: str = ""
