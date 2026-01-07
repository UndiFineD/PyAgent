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
class SearchResult:
    """Result from changelog search.

    Attributes:
        version: Version where match was found.
        line_number: Line number of the match.
        context: Surrounding text context.
        match_score: Relevance score (0 - 1).
    """
    version: str
    line_number: int
    context: str
    match_score: float = 1.0
