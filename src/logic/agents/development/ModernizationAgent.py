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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.types.ModernizationSuggestion import ModernizationSuggestion
import re

__version__ = VERSION




class ModernizationAgent:
    """Advises on modernizing deprecated APIs.

    Tracks deprecated API usage and suggests modern replacements.

    Attributes:
        suggestions: List of modernization suggestions.

    Example:
        >>> advisor=ModernizationAgent()
        >>> suggestions=advisor.analyze("import urllib2")
    """

    DEPRECATIONS: list[tuple[str, str, str, str | None, str]] = [
        (r"import\s+urllib2", "urllib.request", "2.7", "3.0",
         "https://docs.python.org/3/library/urllib.request.html"),
        (r"from\s+collections\s+import\s+.*\bMapping\b",
         "collections.abc.Mapping", "3.3", "3.10",
         "Use collections.abc instead of collections for ABCs"),
        (r'\.encode\s*\(\s*[\'"]hex[\'"]\s*\)',
         "binascii.hexlify()", "3.0", None,
         "Use binascii.hexlify() instead of .encode('hex')"),
        (r"asyncio\.get_event_loop\(\)",
         "asyncio.get_running_loop() or asyncio.new_event_loop()", "3.10", None,
         "get_event_loop() deprecated in favor of more explicit alternatives"),
    ]

    def __init__(self) -> None:
        """Initialize the modernization advisor."""
        self.suggestions: list[ModernizationSuggestion] = []

    def analyze(self, content: str) -> list[ModernizationSuggestion]:
        """Analyze code for deprecated API usage.

        Args:
            content: Source code to analyze.

        Returns:
            List of modernization suggestions.
        """
        self.suggestions = []

        for pattern, new_api, dep_ver, rem_ver, guide in self.DEPRECATIONS:
            if re.search(pattern, content):
                self.suggestions.append(ModernizationSuggestion(
                    old_api=pattern,
                    new_api=new_api,
                    deprecation_version=dep_ver,
                    removal_version=rem_ver,
                    migration_guide=guide
                ))

        return self.suggestions
