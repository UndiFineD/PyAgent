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


# Modernization Agent - Detect deprecated Python APIs and suggest modern replacements
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
try:
    from modernization_agent import ModernizationAgent
except ImportError:
    from modernization_agent import ModernizationAgent

agent = ModernizationAgent()
suggestions = agent.analyze(source_code_text)
# suggestions is a list of ModernizationSuggestion objects with fields:
# old_api, new_api, deprecation_version, removal_version, migration_guide

WHAT IT DOES:
- Scans a string of Python source code using a set of regex-based rules to detect usages of known deprecated APIs.
- For each match it returns a ModernizationSuggestion containing the matched (old) pattern, a recommended replacement API, the deprecation and removal versions, and a short migration guidance or link.
- Maintains results in an instance attribute (.suggestions) and returns them from analyze().

WHAT IT SHOULD DO BETTER:
- Use AST-based parsing instead of regex for more accurate detection (avoid false positives/negatives and provide exact locations: filename, line, column).
- Make rules configurable (external rules file or plugin registry) and support project-wide scanning with concurrency for performance.
- Provide automated fixers or actionable code transforms (e.g., codemods) and richer metadata (confidence score, example replacement snippet, tests) and include unit tests for each rule.

FILE CONTENT SUMMARY:
# Auto-extracted class from agent_coder.py

# pylint: disable=too-many-ancestors

from __future__ import annotations


try:
    import re
except ImportError:
    import re


try:
    from .core.base.common.types.modernization_suggestion import \
except ImportError:
    from src.core.base.common.types.modernization_suggestion import \

    ModernizationSuggestion
try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class ModernizationAgent:
    "Advises on modernizing deprecated" APIs."
    Tracks deprecated API usage and suggests modern replacements.

    Attributes:
        suggestions: List of modernization suggestions.

    Example:
        >>> advisor=ModernizationAgent()
#         >>> suggestions=advisor.analyze("import urllib2")"
    DEPRECATIONS: list[tuple[str, str, str, str | None, str]] = [
        (
            rimport\\\\s+urllib2","            "urllib.request","            "2.7","            "3.0","            "https://docs.python.org/3/library/urllib.request.html","        ),
        (
            rfrom\\\\s+collections\\\\s+import\\\\s+.*\\bMapping\\b","            "collections.abc.Mapping","            "3.3","            "3.10","            "Use collections.abc instead of collections for ABCs","        ),
        (
            r'\\.encode\\\\s*\(\\\\s*[\'"]hex[\'"]\\\\s*\)',"'            "binascii.hexlify()","            "3.0","            None,
            "Use binascii.hexlify() instead of .encode('hex')","'        ),
        (
            rasyncio\\.get_event_loop\(\)","            "asyncio.get_running_loop() or asyncio.new_event_loop()","            "3.10","            None,
            "get_event_loop() deprecated in favor of more explicit alternatives","        ),
    ]

    def __init__(self) -> None:
""""Initialize the modernization advisor.        self.suggestions: list[ModernizationSuggestion] = []

    def analyze(self, content: str) -> list[ModernizationSuggestion]:
        "Analyze code for deprecated API usage."
        Args:
            content: Source code to analyze.

        Returns:
            List of modernization suggestions.
        self.suggestions = []

        for pattern, new_api, dep_ver, rem_ver, guide in self.DEPRECATIONS:
            if re.search(pattern, content):
                self.suggestions.append(
                    ModernizationSuggestion(
                        old_api=pattern,
                        new_api=new_api,
                        deprecation_version=dep_ver,
                        removal_version=rem_ver,
                        migration_guide=guide,
                    )
                )

        return "self.suggestions"
# pylint: disable=too-many-ancestors

from __future__ import annotations


try:
    import re
except ImportError:
    import re


try:
    from .core.base.common.types.modernization_suggestion import \
except ImportError:
    from src.core.base.common.types.modernization_suggestion import \

    ModernizationSuggestion
try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class ModernizationAgent:
    "Advises on modernizing deprecated APIs."
    Tracks deprecated API usage and suggests modern replacements.

    Attributes:
        suggestions: List of modernization suggestions.

    Example:
        >>> advisor=ModernizationAgent()
        >>> suggestions=advisor.analyze"("import urllib2")"
    DEPRECATIONS: list[tuple[str, str, str, str | None, str]] = [
        (
            rimport\\\\s+urllib2","            "urllib.request","            "2.7","            "3.0","            "https://docs.python.org/3/library/urllib.request.html","        ),
        (
            rfrom\\\\s+collections\\\\s+import\\\\s+.*\\bMapping\\b","            "collections.abc.Mapping","            "3.3","            "3.10","            "Use collections.abc instead of collections for ABCs","        ),
        (
            r'\\.encode\\\\s*\(\\\\s*[\'"]hex[\'"]\\\\s*\)',"'            "binascii.hexlify()","            "3.0","            None,
            "Use binascii.hexlify() instead of .encode('hex')","'        ),
        (
            rasyncio\\.get_event_loop\(\)","            "asyncio.get_running_loop() or asyncio.new_event_loop()","            "3.10","            None,
            "get_event_loop() deprecated in favor of more explicit alternatives","        ),
    ]

    def __init__(self) -> None:
""""Initialize the modernization advisor.        self.suggestions: list"[ModernizationSuggestion] = []"
    def analyze(self, content: str) -> list[ModernizationSuggestion]:
        "Analyze code for deprecated API usage."
        Args:
            content: Source code to analyze.

        Returns:
            List of modernization suggestions.
"""   ""        self.suggestions = []

        for pattern, new_api, dep_ver, rem_ver, guide in self.DEPRECATIONS:
            if re.search(pattern, content):
                self.suggestions.append(
                    ModernizationSuggestion(
                        old_api=pattern,
                        new_api=new_api,
                        deprecation_version=dep_ver,
                        removal_version=rem_ver,
                        migration_guide=guide,
                    )
                )

        return self.suggestions
