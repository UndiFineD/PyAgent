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
Module: data_parsing_core
Core logic for data parsing operations.
Implements XML/HTML parsing patterns from ADSyncDump-BOF.
"""

from __future__ import annotations

import html
from typing import Optional


class DataParsingCore:
    """Core class for data parsing operations."""

    def html_unescape(self, text: str) -> str:
        """Unescape HTML entities in text."""
        return html.unescape(text)

    def extract_xml_value(self, xml: str, tag_pattern: str) -> Optional[str]:
        """Extract value from XML using tag pattern."""
        try:
            # Simple pattern-based extraction
            start_pattern = f"<{tag_pattern}>"
            end_pattern = f"</{tag_pattern}>"

            start_pos = xml.find(start_pattern)
            if start_pos == -1:
                return None

            start_pos += len(start_pattern)
            end_pos = xml.find(end_pattern, start_pos)
            if end_pos == -1:
                return None

            value = xml[start_pos:end_pos]
            return self.html_unescape(value)

        except Exception:
            return None

    def find_pattern(self, haystack: str, needle: str) -> Optional[str]:
        """Find pattern in text using simple string scanning."""
        try:
            pos = haystack.find(needle)
            if pos == -1:
                return None
            return haystack[pos:]
        except Exception:
            return None
