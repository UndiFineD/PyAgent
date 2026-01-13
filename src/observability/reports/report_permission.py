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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .PermissionLevel import PermissionLevel
from dataclasses import dataclass
from typing import Optional

__version__ = VERSION

@dataclass
class ReportPermission:
    """Permission for report access.
    Attributes:
        user_id: User identifier.
        report_pattern: Glob pattern for reports.
        level: Permission level.
        granted_by: Who granted permission.
        expires_at: Expiration timestamp.
    """

    user_id: str
    report_pattern: str
    level: PermissionLevel = PermissionLevel.READ
    granted_by: str = ""
    expires_at: Optional[float] = None