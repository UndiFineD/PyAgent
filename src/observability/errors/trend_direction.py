#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
trend_direction.py - TrendDirection Enum

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Minimal import: from trend_direction import TrendDirection
- When used inside package: from src.core.base.agent_errors.trend_direction import TrendDirection
- Example: if direction == TrendDirection.INCREASING: handle_uptrend()

WHAT IT DOES:
Defines a simple Enum, TrendDirection, with four named members (INCREASING, DECREASING, STABLE, VOLATILE) and exposes module version via __version__ imported from lifecycle.VERSION. Intended as a canonical set of labels for representing observed trend directions in higher-level agent logic or telemetry.

WHAT IT SHOULD DO BETTER:
- Add a module-level docstring describing intent, provenance and recommended usage site (why it was extracted from agent_errors.py).
- Provide helper constructors/parsers (e.g., from_delta, from_string, and a normalization function) to map numeric changes or free-form text into these enum values.
- Add explicit __all__ export, unit tests covering string round-trips and parsing, and richer member docstrings or comments explaining when to use VOLATILE vs STABLE.
- Consider making it pluggable/configurable (thresholds for STABLE vs VOLATILE) rather than fixed labels, and include typing stubs or pydantic models when used in public APIs.

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TrendDirection(Enum):
    """Trend direction indicators."""

    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TrendDirection(Enum):
    """Trend direction indicators."""

    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"
