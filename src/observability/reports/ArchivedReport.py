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
from src.core.base.Version import VERSION
from dataclasses import dataclass, field
from typing import Any
import time

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
