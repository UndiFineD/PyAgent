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
PermissionLevel - Enum of report access levels

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- from src.core.models.permission_level import PermissionLevel
- Use to represent access rights: if level >= PermissionLevel.READ: allow read access.
- Persist numeric value (e.g., in DB) or map to RBAC scopes for enforcement.

WHAT IT DOES:
Defines a simple, explicit enumeration of permission tiers (NONE, READ, WRITE, ADMIN) used to control access to generated reports and related operations. It centralizes numeric values for comparisons and storage and provides a clear, minimal contract for permission checks across the codebase.

WHAT IT SHOULD DO BETTER:
- Provide helper methods for common checks (is_readable, is_writable, is_admin) and for safe parsing/serialization from strings or ints.
- Integrate with a broader RBAC/scope model (mapping enums to granular scopes or capability sets) instead of relying solely on ordinal comparisons.
- Add unit tests, type annotations for exported API surfaces, and optional metadata (human-readable labels, descriptions) to improve UX and localization support.
- Consider using bitflags if combinations of permissions are needed, and provide JSON (de)serialization helpers for API payloads.

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

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class PermissionLevel(Enum):
    """Permission levels for report access."""

    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 3
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class PermissionLevel(Enum):
    """Permission levels for report access."""

    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 3
