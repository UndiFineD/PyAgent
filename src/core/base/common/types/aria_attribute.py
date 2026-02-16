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

"""Auto-extracted class from agent_coder.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ARIAAttribute:
    """ARIA attribute definition.

    Attributes:
        name: ARIA attribute name (e.g., "aria-label").
        value: Current value.
        is_valid: Whether the value is valid.
        allowed_values: List of allowed values (if constrained).
        suggestion: Suggested improvement.
    """

    name: str
    value: str = ""
    is_valid: bool = True
    allowed_values: list[str] = field(default_factory=lambda: [])
    suggestion: str | None = None
