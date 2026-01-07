#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

@dataclass
class LocalizedString:
    """Localized string with translations.
    Attributes:
        key: String key.
        translations: Locale to text mapping.
        default: Default text if locale missing.
    """

    key: str
    translations: Dict[str, str] = field(default_factory=dict)  # type: ignore[assignment]
    default: str = ""
