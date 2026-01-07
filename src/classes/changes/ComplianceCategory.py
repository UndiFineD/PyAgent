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

class ComplianceCategory(Enum):
    """Categories for compliance checking."""
    SECURITY = "security"
    LEGAL = "legal"
    PRIVACY = "privacy"
    ACCESSIBILITY = "accessibility"
