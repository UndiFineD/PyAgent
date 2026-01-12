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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import os
import re
import json
import logging
from typing import Dict, List, Any, Optional
from src.core.base.BaseAgent import BaseAgent


class LocalizationAgent(BaseAgent):
    """
    Handles localization and internationalization (i18n) tasks.
    Helps in extracting translatable strings and managing translation files.
    """
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.supported_locales = ["en", "es", "fr", "de", "zh"]

    def extract_strings(self, file_path: str) -> List[str]:
        """Extracts potential user-facing strings for translation."""
        # Simple heuristic for potential translatable strings
        # (e.g., strings in print() or gettext calls)
        found_strings = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Matches gettext style calls _("string") or _('string')
                matches = re.finditer(r'_\(["\'](.*?)["\']\)', content)
                for match in matches:
                    found_strings.append(match.group(1))
        except Exception as e:
            logging.error(f"LocalizationAgent: Error reading {file_path}: {e}")
        return found_strings

    def generate_translation_file(self, locale: str, strings: List[str]) -> Dict[str, str]:
        """Generates a JSON translation dictionary for a specific locale."""
        if locale not in self.supported_locales:
            logging.warning(f"Locale {locale} not officially supported.")
        
        translation_map = {s: f"TRANSLATED_{locale}_{s}" for s in strings}
        return translation_map

    def solve_translation_task(self, prompt: str) -> str:
        """Uses LLM to help with complex translation tasks."""
        return self.improve_content(f"Translate the following content preserving formatting: {prompt}")
