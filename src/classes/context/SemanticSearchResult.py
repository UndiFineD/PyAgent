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
class SemanticSearchResult:
    """Result from semantic code search.

    Attributes:
        file_path: Path to the matching file.
        content_snippet: Relevant code snippet.
        similarity_score: Similarity score (0 - 1).
        context_type: Type of context matched.
        line_range: Tuple of start and end line numbers.
    """
    file_path: str
    content_snippet: str
    similarity_score: float
    context_type: str = ""
    line_range: Tuple[int, int] = (0, 0)
