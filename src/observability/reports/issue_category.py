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
IssueCategory - Enum for classifying code issues

[Brief Summary]
A small, focused enum that centralizes canonical issue categories used across reporting and analysis subsystems. Keeps category strings consistent and versioned via the project's VERSION constant.

DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from issue_category import IssueCategory
# compare or iterate
if IssueCategory.SYNTAX == IssueCategory("syntax"):
    ...

WHAT IT DOES:
Defines IssueCategory, an Enum of common code issue categories (syntax, typing, style, security, performance, documentation) and exposes module __version__ tied to the project VERSION.

WHAT IT SHOULD DO BETTER:
- Add module-level tests exercising serialization/deserialization and membership checks.
- Provide a stable import path and explicit exports (e.g., __all__).
- Include helper utilities (e.g., severity mapping, human-readable labels, list/choices for forms) and documentation explaining intended use across subsystems.
- Consider using StrEnum (or IntEnum with explicit severities) and richer typing to ease integration.

FILE CONTENT SUMMARY:

"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class IssueCategory(Enum):
    """Category of code issue."""

    SYNTAX = "syntax"
    TYPE_ANNOTATION = "type_annotation"
    STYLE = "style"
    SECURITY = "security"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
