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
SeverityLevel - Defines severity enumeration for issues

# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Example:
from src.core.base.severity_level import SeverityLevel
if issue.severity is SeverityLevel.ERROR:
    handle_error(issue)
print(SeverityLevel.WARNING.name, SeverityLevel.WARNING.value)

WHAT IT DOES:
Defines a small, explicit Enum mapping named severity levels (INFO, WARNING, ERROR, CRITICAL) used across the codebase, and exposes module version via the imported VERSION constant.

WHAT IT SHOULD DO BETTER:
- Provide richer integration with Python logging (mapping to logging levels) and with serialization (to/from JSON or DB).
- Add ordering and utility helpers (e.g., is_at_least, to_int, from_int) and explicit unit tests.
- Improve module docstring and include examples and type hints for consumers.

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
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SeverityLevel(Enum):
    """Severity level for issues."""

    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
