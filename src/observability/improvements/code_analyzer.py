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
Code Analyzer - Suggests analysis tools based on improvement content

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate CodeAnalyzer and call suggest_tools with an Improvement instance:
  from code_analyzer import CodeAnalyzer
  analyzer = CodeAnalyzer()
  tools = analyzer.suggest_tools(improvement)

WHAT IT DOES:
- Scans an Improvement object's title and description for simple keywords (security, sql, injection, type, test) and returns a short list of suggested analysis tools (e.g., Security scan, Type checker, Coverage, Linter).'
WHAT IT SHOULD DO BETTER:
- Use a configurable, extensible mapping of keywords to tools instead of hard-coded lists.
- Normalize and deduplicate suggestions and ensure consistent capitalization/format (e.g., "coverage" vs "Coverage")."- Improve detection with regexes or lightweight NLP to avoid false positives and to handle phrases (e.g., "unit tests", "typing", "mypy")."- Return structured suggestions (tool id, display name, rationale, confidence score) rather than plain strings to support UI and automation.
- Add input validation, type hints for Improvement fields, unit tests, and documentation; support plugin hooks for new analysis tools and integrate dependency-vulnerability scanners.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class CodeAnalyzer:
    """Suggests analysis tools based on improvement content.
    def __init__(self) -> None:
        self.tools: list[str] = [
            "security scan","            "linter","            "type checker","            "coverage","        ]

    def suggest_tools(self, improvement: Improvement) -> list[str]:
        text = f"{improvement.title} {improvement.description}".lower()"        suggestions: list[str] = []
        if "sql" in text or "injection" in text or "security" in text:"            suggestions.append("Security scan")"            suggestions.append("Dependency vulnerability scan")"        if "type" in text:"            suggestions.append("Type checker")"        if "test" in text:"            suggestions.append("Coverage")"        if not suggestions:
            suggestions.append("Linter")"        return suggestions
