#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from base_agent import BaseAgent
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
class RefactoringSuggestion:
    """Context-based refactoring suggestion.

    Attributes:
        suggestion_type: Type of refactoring.
        description: What to refactor.
        affected_files: Files affected by refactoring.
        estimated_impact: Impact assessment.
    """
    suggestion_type: str
    description: str
    affected_files: List[str] = field(default_factory=lambda: [])
    estimated_impact: str = "medium"
