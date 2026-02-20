#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Auto-extracted class from agent_coder.py
"""
try:

"""
from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.common.types.migration_status import MigrationStatus
except ImportError:
    from src.core.base.common.types.migration_status import MigrationStatus

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class MigrationRule:
"""
A rule for code migration from old to new API.

    Attributes:
        name: Rule identifier.
        old_pattern: Regex pattern to match old API usage.
        new_pattern: Replacement pattern for new API.
        description: Human-readable description of the migration.
        status: Current status of this migration rule.
        breaking_change: Whether this is a breaking change.
"""
name: str
    old_pattern: str
    new_pattern: str
    description: str
    status: MigrationStatus = MigrationStatus.PENDING
    breaking_change: bool = False
