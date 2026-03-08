#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/reports/report_cache.description.md

# Description: src/observability/reports/report_cache.py

Module overview:
- `ReportCache` dataclass represents a cached report entry with metadata such as path, content hash, TTL, and creation timestamp.

Behavioral notes:
- Simple in-memory data container; persistence and management are handled by `ReportCacheManager`.
## Source: src-old/observability/reports/report_cache.improvements.md

# Improvements: src/observability/reports/report_cache.py

Suggested improvements (automatically generated):
- Add unit tests covering core behavior and edge cases.
- Break large modules into smaller, testable components.
- Avoid heavy imports at module import time; import lazily where appropriate.
- Add type hints and explicit return types for public functions.
- Add logging and better error handling for file and IO operations.
- Consider dependency injection for filesystem and environment interactions.

LLM_CONTEXT_END
"""

from __future__ import annotations
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


"""Auto-extracted class from generate_agent_reports.py"""


from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ReportCache:
    """Cache for report data.
    Attributes:
        path: File path for the cached report.
        content_hash: Hash of the cached content.
        content: The cached report content.
        created_at: Timestamp when cache was created.
        ttl_seconds: Time - to - live for cache entries.
    """

    path: str = ""
    content_hash: str = ""
    content: str = ""
    created_at: float = 0.0
    ttl_seconds: int = 3600
