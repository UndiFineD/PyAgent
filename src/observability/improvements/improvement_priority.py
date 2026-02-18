#!/usr/bin/env python3
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
Improvement Priority - Defines priority levels for agent improvements

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
try:
    from .core.base.improvement_priority import ImprovementPriority
except ImportError:
    from src.core.base.improvement_priority import ImprovementPriority

# use as ImprovementPriority.CRITICAL, .HIGH, etc., or compare by value

WHAT IT DOES:
Provides a small, explicit Enum (ImprovementPriority) that encodes five discrete priority levels for improvements and exposes module version via __version__.

WHAT IT SHOULD DO BETTER:
- Provide helper methods for serialization/deserialization (to/from string, JSON) and stable ordering helpers.
- Add mappings to SLAs, default remediation timelines, or numeric severity metadata for integration with scoring systems.
- Include unit tests, richer docstrings on members, and an explicit __all__ export; consider freezing the API to avoid accidental reordering or renumbering.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations


try:
    from enum import Enum
except ImportError:
    from enum import Enum


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class ImprovementPriority(Enum):
    """Priority levels for improvements.    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NICE_TO_HAVE = 1
