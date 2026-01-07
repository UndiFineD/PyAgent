#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .ImportSource import ImportSource

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
class ImportedEntry:
    """An entry imported from external source.

    Attributes:
        source: Where the entry was imported from.
        external_id: ID in the external system.
        title: Entry title.
        description: Entry description.
        author: Author of the entry.
        created_at: When the entry was created.
        labels: Labels / tags from the source.
    """
    source: ImportSource
    external_id: str
    title: str
    description: str
    author: str = ""
    created_at: str = ""
    labels: List[str] = field(default_factory=lambda: [])
