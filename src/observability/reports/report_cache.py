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

"""ReportCache - Cache for report data.

DATE: 2026-02-12
AUTHOR: Keimpe de Jong

USAGE:
    Instantiate as a lightweight container:
        cache = ReportCache(
            path="reports/weekly.md",
            content="...",
            content_hash="sha256...",
            created_at=time.time()
        )
    Check expiry:
        expired = (time.time() - cache.created_at) > cache.ttl_seconds
    Update when regenerating a report:
        set content, recompute content_hash, and set created_at = time.time()

WHAT IT DOES:
    Provides a minimal dataclass to hold cached report metadata and content
    (file path, content hash, raw content, creation timestamp, and a TTL in
    seconds) intended for short-lived in-memory or transient-file caching of
    generated reports.

WHAT IT SHOULD DO BETTER:
    - Add methods: is_expired(), refresh(new_content), to_dict()/from_dict(),
      and persistence helpers (save/load) to avoid ad-hoc external handling.
    - Use datetime/datetime.timedelta for clearer time semantics and
      timezone-awareness.
    - Provide validation and stronger typing (Optional[str] where
      appropriate), and integrate hashing utilities rather than requiring
      callers to set content_hash.
    - Consider concurrency safety (thread/process locks) and pluggable
      backends (memory, disk, redis) for scaling.
"""

from __future__ import annotations


try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class ReportCache:
    """
    Cache for report data.

    Attributes:
        path: File path for the cached report.
        content_hash: Hash of the cached content.
        content: The cached report content.
        created_at: Timestamp when cache was created.
        ttl_seconds: Time-to-live for cache entries.
    """
    path: str = ""
    content_hash: str = ""
    content: str = ""
    created_at: float = 0.0
    ttl_seconds: int = 3600

    #     Instantiate as a lightweight container:
    #    cache = ReportCache(
    #        path="reports/weekly.md",
    #        content="...",
    #        content_hash="sha256...",
    #        created_at=time.time()
    #    )
    #
    #def __init__ (path,content, content_hash, created_at):
