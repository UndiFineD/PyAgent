#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from src.logic.agents.cognitive.context.models.ExportFormat import ExportFormat

from src.core.base.BaseAgent import BaseAgent
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
class ExportedContext:
    """Exported context document.

    Attributes:
        format: Export format used.
        content: Exported content.
        metadata: Export metadata.
        created_at: Creation timestamp.
    """
    format: ExportFormat
    content: str
    metadata: Dict[str, Any] = field(default_factory=lambda: {})
    created_at: str = ""
