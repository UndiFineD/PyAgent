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
CompileResult - Result of compile / syntax check

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.core.base.lifecycle.compile_result import CompileResult
result = CompileResult(ok=True)            # success
result = CompileResult(ok=False, error="SyntaxError: invalid syntax")  # failure

WHAT IT DOES:
Provides an immutable dataclass that represents the outcome of a compile or syntax check: a boolean 'ok' and an optional 'error' message string.

WHAT IT SHOULD DO BETTER:
- Include richer error metadata (exception type, traceback, filename, line number) instead of a plain string.
- Add convenience methods for serialization (to_dict/from_dict) and logging helpers for consistent output.
- Validate inputs (e.g., ensure error is None when ok is True) and supply unit tests and docstrings for public API clarity.

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

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass(frozen=True)
class CompileResult:
    """Result of compile / syntax check."""

    ok: bool
    error: str | None = None
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass(frozen=True)
class CompileResult:
    """Result of compile / syntax check."""

    ok: bool
    error: str | None = None
