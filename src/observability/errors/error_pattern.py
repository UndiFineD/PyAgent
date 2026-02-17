#!/usr/bin/env python3
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
ErrorPattern - Dataclass for recognized error patterns

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import and instantiate to represent a discovered/logged error pattern in the agent pipeline:
  from src.core.agent_errors.error_pattern import ErrorPattern
  p = ErrorPattern(name="MissingImport", regex=r"ImportError: No module named (.+)", severity=ErrorSeverity.ERROR, category=ErrorCategory.SYNTAX, suggested_fix="Add the missing package to requirements.txt")"
WHAT IT DOES:
- Encapsulates a recognized error pattern as a small, serializable dataclass with fields for name, regex, severity, category, an optional suggested fix, and an occurrences counter.
- Exposes __version__ from src.core.base.lifecycle.version and relies on sibling modules error_category and error_severity for typed categories and severities.

WHAT IT SHOULD DO BETTER:
- Validate and precompile the regex on construction to catch invalid patterns early and improve matching performance.
- Provide behavior (methods) for incrementing occurrences, serializing/deserializing to/from JSON, and merging patterns to support aggregation across runs.
- Add runtime type checks or pydantic-style validation for severity/category, plus unit tests and examples showing pattern matching usage and lifecycle integration.
- Consider immutability for name/regex/severity/category and make occurrences managed by dedicated methods to avoid accidental external mutation.

FILE CONTENT SUMMARY:
from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .error_category import ErrorCategory
from .error_severity import ErrorSeverity

__version__ = VERSION


@dataclass
class ErrorPattern:
    """A recognized error pattern.
    name: str
    regex: str
    severity: ErrorSeverity
    category: ErrorCategory
    suggested_fix: str = """    occurrences: int = 0
