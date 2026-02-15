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
transition_result - TransitionResult dataclass

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import: from src.core.base.lifecycle.transition_result import TransitionResult
- Create: result = TransitionResult(success=True, message="migrated")
- Check: if result.success: handle_success() else: handle_failure(result.message)

WHAT IT DOES:
Provides a minimal, serializable container for representing the outcome of a lifecycle/state transition with a boolean success flag and an optional message string. It centralizes the small, common pattern of returning (success, message) tuples as a single typed object and exposes module version via __version__ from the package VERSION constant.

WHAT IT SHOULD DO BETTER:
- Add a docstring describing semantics (e.g., message purpose, expected contents) and intended consumers.
- Validate inputs (e.g., coerce/validate message type) and consider freeze/immutability (frozen dataclass) for safer sharing across agents.
- Extend with standardized error codes or an optional exception field for richer diagnostics, and provide convenience constructors (success()/failure()) and a clear __repr__ or to_dict() for logging/serialization.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class TransitionResult:
    success: bool
    message: str = ""
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class TransitionResult:
    success: bool
    message: str = ""
