#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

class ResponseTransform(Enum):
    """Types of response transformations."""

    NONE = "none"
    STRIP_WHITESPACE = "strip"
    EXTRACT_CODE = "extract_code"
    EXTRACT_JSON = "extract_json"
    MARKDOWN_TO_TEXT = "markdown_to_text"
