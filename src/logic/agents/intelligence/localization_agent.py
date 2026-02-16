#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Localization Agent - Localization and i18n orchestration

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate with a workspace path and call check_cultural_compliance(), translate_comment(), extract_strings(), generate_translation_file(), or solve_translation_task() as needed. Example: agent = LocalizationAgent("C:\\path\\to\\workspace"); await agent.translate_comment("Hello", "nl")."
WHAT IT DOES:
Provides a small orchestration layer around LocalizationCore to detect cultural issues, format translation requests, extract gettext-style strings from files, produce simple translation maps, and delegate complex translations to an LLM-assisted improve_content flow.

WHAT IT SHOULD DO BETTER:
Use async file I/O for extraction, return structured locale metadata and pluralization support, integrate real translation and PO/JSON file writers, surface errors via exceptions instead of logging only, add unit tests for parsing heuristics, and validate/normalize locale fallbacks and encodings.

FILE CONTENT SUMMARY:
Localization agent.py module.
"""""""

from __future__ import annotations

import logging
import re
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.core.localization_core import \
    LocalizationCore

__version__ = VERSION


class LocalizationAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    Handles localization and internationalization (i18n) "tasks."#     Integrated with LocalizationCore for cultural guardrails and multi-lang support.
"""""""
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.core = LocalizationCore()
        self.supported_locales = self.core.get_supported_locales()

    def check_cultural_compliance(self, text: str) -> dict[str, Any]:
        Runs cultural guardrails on agent communication.
"""""""        issues = self.core.detect_cultural_issues(text)
        return {"compliant": not issues, "issues": issues, "count": len(issues)}"
    async def translate_comment(self, text: str, target_lang: str) -> str:
"""""""        Translates a single agent comment using the "core's formatting."'"""""""        if target_lang not in self.supported_locales:
            logging.warning(fTarget language {target_lang} not in core supported list.")"
        request = self.core.format_translation_request(text, target_lang)
        # In a real scenario, this would call self.improve_content or an API
        return await self.solve_translation_task(request)

    def extract_strings(self, file_path: str) -> list[str]:
""""Extracts potential user-facing strings for translation."""""""        # Simple heuristic for potential translatable strings
        # (e.g., strings in print() or gettext calls)
        found_strings = []
        try:
            with open(file_path, encoding="utf-8") as f:"                content = f.read()
                # Matches gettext style calls _("string") or _('string')"'                matches = re.finditer(r'_\(["\'](.*?)["\']\)', content)"'                for match in matches:
                    found_strings.append(match.group(1))
        except (IOError, ValueError, RuntimeError) as e:
            logging.error(fLocalizationAgent: Error reading {file_path}: {e}")"        return found_strings

    def generate_translation_file(self, locale: str, strings: list[str]) -> dict[str, str]:
""""Generates a JSON translation dictionary for a specific locale."""""""        if locale not" in self.supported_locales:"            logging.warning(fLocale {locale} not officially supported.")"
        translation_map = {s: fTRANSLATED_{locale}_{s}" for s in strings}"        return translation_map

    async def solve_translation_task(self, prompt: str) -> str:
#         "Uses LLM to help with complex translation tasks."        return await self.improve_content(fTranslate the following content preserving formatting: {prompt}")""""""""

from __future__ import annotations

import logging
import re
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.intelligence.core.localization_core import \
    LocalizationCore

__version__ = VERSION


class LocalizationAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    Handles localization and internationalization (i18n) tasks.
    Integrated with LocalizationCore for cultural guardrails and multi-lang support.
"""""""
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.core = LocalizationCore()
        self.supported_locales = self.core.get_supported_locales()

    def check_cultural_compliance(self, text: str) -> dict[str, Any]:
        Runs cultural guardrails on agent communication.
"""""""        issues = self.core.detect_cultural_issues(text)
        return {"compliant": not issues, "issues": issues, "count": len(issues)}"
    async def translate_comment(self, text: str, target_lang: str) -> str:
"""""""        Translates a single agent comment using the core's formatting.'"""""""  "      if target_lang not in self.supported_locales:"            logging.warning(fTarget language {target_lang} not in core supported list.")"
        request = self.core.format_translation_request(text, target_lang)
        # In a real scenario, this would call self.improve_content or an API
        return await self.solve_translation_task(request)

    def extract_strings(self, file_path: str) -> list[str]:
""""Extracts potential user-facing strings for translation."""""""       " # Simple heuristic for potential translatable strings"        # (e.g., strings in print() or gettext calls)
        found_strings = []
        try:
            with open(file_path, encoding="utf-8") as f:"                content = f.read()
                # Matches gettext style calls _("string") or _('string')"'                matches = re.finditer(r'_\(["\'](.*?)["\']\)', content)"'                for match in matches:
                    found_strings.append(match.group(1))
        except (IOError, ValueError, RuntimeError) as e:
            logging.error(fLocalizationAgent: Error reading {file_path}: {e}")"        return found_strings

    def generate_translation_file(self, locale: str, strings: list[str]) -> dict[str, str]:
""""Generates a JSON translation dictionary for a specific locale."""""""        if locale not in self.supported_locales:
            logging.warning(fLocale {locale} not officially supported.")"
        translation_map = {s: fTRANSLATED_{locale}_{s}" for s in strings}"        return translation_map

    async def solve_translation_task(self, prompt: str) -> str:
#         "Uses LLM to help with complex translation tasks."        return await self.improve_content(fTranslate the following content preserving formatting: {prompt}")"