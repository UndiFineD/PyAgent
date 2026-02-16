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

"""Auto-extracted class from agent.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.core.base.common.models import LockType
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class FileLock:
    """File lock information.

    Attributes:
        file_path: Path to the locked file.
        lock_type: Type of lock.
        owner: Lock owner identifier.
        acquired_at: Timestamp when lock was acquired.
        expires_at: Timestamp when lock expires (optional).
    """

    file_path: Path
    lock_type: LockType
    owner: str
    acquired_at: float
    expires_at: float | None = None
