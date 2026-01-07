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

@dataclass
class RollbackRecord:
    """Record of an improvement rollback.

    Attributes:
        improvement_id: ID of the rolled back improvement.
        rollback_date: When the rollback occurred.
        reason: Reason for the rollback.
        previous_state: State before the improvement.
        rollback_commit: Git commit of the rollback.
    """
    improvement_id: str
    rollback_date: str = ""
    reason: str = ""
    previous_state: str = ""
    rollback_commit: str = ""
