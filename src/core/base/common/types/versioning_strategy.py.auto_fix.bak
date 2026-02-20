#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Auto-extracted class from agent_changes.py
"""

from enum import Enum

try:
    from src.core.base.lifecycle.version import VERSION
except ImportError:
    from ..lifecycle.version import VERSION

__version__ = VERSION


class VersioningStrategy(Enum):
    """Supported versioning strategies.
    """

    SEMVER = "semver"  # Semantic Versioning (MAJOR.MINOR.PATCH)
    CALVER = "calver"  # Calendar Versioning (YYYY.MM.DD)
    CUSTOM = "custom"  # Custom versioning pattern
