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
error_category.py - ErrorCategory Enum

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.core.base.error_category import ErrorCategory
# Use ErrorCategory.SYNTAX, ErrorCategory.RUNTIME, etc., to classify or tag errors.

WHAT IT DOES:
Defines a compact Enum, ErrorCategory, enumerating common error classifications (syntax, runtime, logic, type, security, performance, style, deprecation, value, import, other) and exposes module version via __version__.

WHAT IT SHOULD DO BETTER:
Add richer documentation for each category, provide mappings to severity/HTTP codes or remediation guidance, include unit tests and type hints for consumers, and consider localization or extensibility (custom categories) and conversion helpers (from string, to human-friendly label).

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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ErrorCategory(Enum):
    """Error categories."""

    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    TYPE = "type"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    DEPRECATION = "deprecation"
    VALUE = "value"
    IMPORT = "import"
    OTHER = "other"
"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ErrorCategory(Enum):
    """Error categories."""

    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    TYPE = "type"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    DEPRECATION = "deprecation"
    VALUE = "value"
    IMPORT = "import"
    OTHER = "other"
