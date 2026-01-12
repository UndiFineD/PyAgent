#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_backend.py"""




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

class ExtractCodeTransformer(ResponseTransformerBase):
    """Transformer that extracts code blocks from markdown."""

    def transform(self, response: str) -> str:
        """Extract code blocks from markdown response.

        Args:
            response: Markdown response with code blocks.

        Returns:
            str: Extracted code without markdown fencing.
        """
        # Match ```language\ncode\n``` blocks
        code_pattern = r"```(?:\w+)?\n(.*?)```"
        matches = re.findall(code_pattern, response, re.DOTALL)
        if matches:
            return "\n\n".join(matches)
        return response.strip()

    def get_name(self) -> str:
        """Get transformer name."""
        return "extract_code"
