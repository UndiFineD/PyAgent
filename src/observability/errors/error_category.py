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



error_category.py - ErrorCategory Enum

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # [Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
# USAGE:
from src.core.base.error_category import ErrorCategory
# Use ErrorCategory.SYNTAX, ErrorCategory.RUNTIME, etc., to classify or tag errors.

# WHAT IT DOES:
# Defines a compact Enum, ErrorCategory, enumerating common error classifications (syntax, runtime, logic, type, security, performance, style, deprecation, value, import, other) and exposes module version via __version__.

# WHAT IT SHOULD DO BETTER:
# Add richer documentation for each category, provide mappings to severity/HTTP codes or remediation guidance, include unit tests and type hints for consumers, and consider localization or extensibility (custom categories) and conversion helpers (from string, to human-friendly label).

# FILE CONTENT SUMMARY:
Auto-extracted class from agent_errors.py


from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ErrorCategory(Enum):
    Error categories.

# [BATCHFIX] Commented metadata/non-Python
# # #     SYNTAX = "syntax"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     RUNTIME = "runtime"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     LOGIC = "logic"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     TYPE = "type"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     SECURITY = "security"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     PERFORMANCE = "performance"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     STYLE = "style"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     DEPRECATION = "deprecation"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     VALUE = "value"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     IMPORT = "import"  # [BATCHFIX] closed string
# #     OTHER = other


from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ErrorCategory(Enum):
    Error categories.

# [BATCHFIX] Commented metadata/non-Python
# # #     SYNTAX = "syntax"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     RUNTIME = "runtime"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     LOGIC = "logic"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     TYPE = "type"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     SECURITY = "security"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     PERFORMANCE = "performance"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     STYLE = "style"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     DEPRECATION = "deprecation"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     VALUE = "value"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     IMPORT = "import"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #     OTHER = "other"  # [BATCHFIX] closed string
