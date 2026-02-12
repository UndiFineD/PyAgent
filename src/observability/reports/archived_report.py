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
archived_report.py - ArchivedReport dataclass for archived report storage and retention

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import ArchivedReport and instantiate with report_id, file_path and content when archiving a generated report.
- Use archived_at for archive timestamp, retention_days to determine TTL, and metadata for additional indexing or search fields.
- Typical usage: from src.some.module import ArchivedReport; r = ArchivedReport(report_id='id', file_path='path', content='...') then persist r to storage.

WHAT IT DOES:
- Provides a minimal, serializable dataclass representing an archived report and its retention metadata.
- Supplies sensible defaults: archived_at defaults to now, retention_days defaults to 90, and metadata defaults to an empty dict.
- Centralizes report identity, content location, archive timestamp and retention policy in a single lightweight object.

WHAT IT SHOULD DO BETTER:
- Add validation (types/values) for fields like report_id, file_path and retention_days and provide clearer error messages.
- Implement serialization helpers (to_dict/from_dict/JSON) and safe persistence hooks to ensure consistent storage and retrieval across backends.
- Expose retention utilities (is_expired, expires_at) and unit tests covering edge cases (large content, timezone-aware timestamps, negative retention_days).
- Consider immutability or frozen dataclass variant for integrity guarantees and include docstring examples showing intended persistence and restore workflows.

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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ArchivedReport:
    """Archived report with retention info.
    Attributes:
        report_id: Unique report identifier.
        file_path: Original file path.
        content: Report content.
        archived_at: Archive timestamp.
        retention_days: Days to retain.
        metadata: Report metadata.
    """

    report_id: str
    file_path: str
    content: str
    archived_at: float = field(default_factory=time.time)  # type: ignore[assignment]
    retention_days: int = 90
    metadata: dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ArchivedReport:
    """Archived report with retention info.
    Attributes:
        report_id: Unique report identifier.
        file_path: Original file path.
        content: Report content.
        archived_at: Archive timestamp.
        retention_days: Days to retain.
        metadata: Report metadata.
    """

    report_id: str
    file_path: str
    content: str
    archived_at: float = field(default_factory=time.time)  # type: ignore[assignment]
    retention_days: int = 90
    metadata: dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]
