#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .LocalizationLanguage import LocalizationLanguage

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
class LocalizedEntry:
    """A changelog entry with localization support.

    Attributes:
        original_text: Original entry text.
        language: Source language of the entry.
        translations: Dictionary of translations by language code.
        auto_translated: Whether translations were auto - generated.
    """
    original_text: str
    language: LocalizationLanguage = LocalizationLanguage.ENGLISH
    translations: Dict[str, str] = field(default_factory=lambda: {})
    auto_translated: bool = False
