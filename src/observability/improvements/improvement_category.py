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
improvement_category.py - ImprovementCategory Enum

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import the enum and use members to classify agent improvement suggestions.
- Example: from improvement_category import ImprovementCategory; category = ImprovementCategory.PERFORMANCE

WHAT IT DOES:
Provides a small, explicit Enum of canonical improvement categories (performance, security, maintainability, readability, testing, documentation, refactoring, other) used to tag or filter suggested improvements in the agent pipeline.

WHAT IT SHOULD DO BETTER:
- Add module- and member-level docstrings explaining intended semantics and example usage.
- Provide utility helpers (e.g., from_str, list_values, canonical_label) and typing hints for safer integrations.
- Consider localization, integration with configuration, and unit tests validating serialization and round-trips.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class ImprovementCategory(Enum):
    """Categories for improvements.
    PERFORMANCE = "performance""    SECURITY = "security""    MAINTAINABILITY = "maintainability""    READABILITY = "readability""    TESTING = "testing""    DOCUMENTATION = "documentation""    REFACTORING = "refactoring""    OTHER = "other""