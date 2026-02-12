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
audit_action.py - Define AuditAction enum for audit logging

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Import the enum and use values when recording audit events to ensure consistent action names across the codebase.
- Example: from src.core.base.audit_action import AuditAction; log_event(action=AuditAction.CREATE.value, actor=user_id, target=resource_id)

WHAT IT DOES:
- Provides a small, explicit Enum (AuditAction) for common CRUD + export actions used in audit logs.
- Centralizes the canonical string values ("create", "read", "update", "delete", "export") to avoid magic strings and typos.

WHAT IT SHOULD DO BETTER:
- Expand or make extensible (e.g., register custom actions) so domain-specific audit events can be added without editing the enum.
- Document expected payloads and integration points (where to call these enums when logging, which logger/transport to use).
- Add unit tests validating serialization, string values, and usage in the audit subsystem; consider integrating with TypedDict or dataclass for audit record structure.
- Consider internationalization or mapping to human-readable labels and severity levels for downstream reporting.

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


class AuditAction(Enum):
    """Actions for audit logging."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class AuditAction(Enum):
    """Actions for audit logging."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
