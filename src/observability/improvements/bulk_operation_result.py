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
BulkOperationResult - Data container for bulk operation outcomes

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Import and instantiate BulkOperationResult to record the number of successful items in a batch, e.g. BulkOperationResult(success_count=5).

WHAT IT DOES:
Provides a minimal dataclass BulkOperationResult with a single integer field success_count and exposes __version__ from src.core.base.lifecycle.version.

WHAT IT SHOULD DO BETTER:
Add failure_count and error detail fields, input validation and type enforcement, convenience methods for merging/serializing results, and unit tests to cover typical aggregation scenarios.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class BulkOperationResult:
    success_count: int
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class BulkOperationResult:
    success_count: int
