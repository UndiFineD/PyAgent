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

class ResponseTransformerBase(ABC):
    """Abstract base class for response transformers.

    Implement this to create custom response transformation logic.
    """

    @abstractmethod
    def transform(self, response: str) -> str:
        """Transform a response string.

        Args:
            response: Raw response string.

        Returns:
            str: Transformed response.
        """

    @abstractmethod
    def get_name(self) -> str:
        """Get transformer name."""
