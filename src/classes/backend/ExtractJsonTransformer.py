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

class ExtractJsonTransformer(ResponseTransformerBase):
    """Transformer that extracts JSON from response."""

    def transform(self, response: str) -> str:
        """Extract JSON from response.

        Args:
            response: Response possibly containing JSON.

        Returns:
            str: Extracted JSON string.
        """
        # Try to find JSON object or array
        json_pattern = r"(\{[^{}]*\}|\[[^\[\]]*\])"
        matches = re.findall(json_pattern, response, re.DOTALL)
        for match in matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
        return response.strip()

    def get_name(self) -> str:
        """Get transformer name."""
        return "extract_json"
