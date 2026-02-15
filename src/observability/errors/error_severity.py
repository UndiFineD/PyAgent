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


"""
ErrorSeverity - Enumeration of error severity levels

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import and use as a stable, project-wide severity enum: from src.core.base.error_severity import ErrorSeverity
- Compare levels: if event_severity >= ErrorSeverity.HIGH: handle_urgent(event)

WHAT IT DOES:
Provides a small, explicit Enum (ErrorSeverity) representing five discrete severity levels (CRITICAL, HIGH, MEDIUM, LOW, INFO) with integer values for ordering and comparison.

WHAT IT SHOULD DO BETTER:
- Add rich-comparison helpers or a utility wrapper to make ordinal comparisons and threshold checks more ergonomic and type-safe.
- Provide mappings to logging levels, human-readable labels, and JSON (de)serialization methods for configuration and transport.
- Include unit tests and examples showing intended comparison semantics and integration with the project's logging and alerting subsystems.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_errors.py
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ErrorSeverity(Enum):
    """Error severity levels."""

    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ErrorSeverity(Enum):
    """Error severity levels."""

    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1
