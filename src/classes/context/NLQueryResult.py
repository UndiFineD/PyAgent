#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

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
class NLQueryResult:
    """Result from natural language query.

    Attributes:
        query: Original query string.
        answer: Generated answer.
        relevant_contexts: List of relevant context files.
        confidence: Confidence score (0 - 1).
    """
    query: str
    answer: str
    relevant_contexts: List[str] = field(default_factory=lambda: [])
    confidence: float = 0.0
