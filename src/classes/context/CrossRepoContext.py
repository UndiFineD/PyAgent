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
class CrossRepoContext:
    """Context from cross-repository analysis.

    Attributes:
        repo_name: Name of the repository.
        repo_url: URL to the repository.
        related_files: List of related file paths.
        similarity_score: Overall similarity score.
        common_patterns: Patterns shared between repos.
    """
    repo_name: str
    repo_url: str
    related_files: List[str] = field(default_factory=lambda: [])
    similarity_score: float = 0.0
    common_patterns: List[str] = field(default_factory=lambda: [])
