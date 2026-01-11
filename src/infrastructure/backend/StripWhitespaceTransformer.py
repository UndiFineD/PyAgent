#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .ResponseTransformerBase import ResponseTransformerBase

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

class StripWhitespaceTransformer(ResponseTransformerBase):
    """Transformer that strips whitespace."""

    def transform(self, response: str) -> str:
        """Strip leading and trailing whitespace."""
        return response.strip()

    def get_name(self) -> str:
        """Get transformer name."""
        return "strip_whitespace"
