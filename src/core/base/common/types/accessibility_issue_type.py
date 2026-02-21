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


"""Accessibility issue type definitions (parser-safe).

This module provides a small Enum used by tests and other modules.
"""
from __future__ import annotations

from enum import Enum

class AccessibilityIssueType(str, Enum):
    MISSING_ALT_TEXT = "missing_alt_text"
    LOW_COLOR_CONTRAST = "low_color_contrast"
    MISSING_LABEL = "missing_label"
    KEYBOARD_NAVIGATION = "keyboard_navigation"
    FOCUS_MANAGEMENT = "focus_management"
    ARIA_MISSING = "aria_missing"
    ARIA_INVALID = "aria_invalid"
    HEADING_HIERARCHY = "heading_hierarchy"
    FORM_VALIDATION = "form_validation"
    SEMANTIC_HTML = "semantic_html"