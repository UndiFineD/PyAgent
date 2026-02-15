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
Changelog Localizer - Localize changelog entries into multiple languages

DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate ChangelogLocalizer(default_language=LocalizationLanguage.ENGLISH).
- Create entries with create_entry("text") which returns a LocalizedEntry.
- Add translations with add_translation(entry, LocalizationLanguage.SPANISH, "texto").
- Render a localized changelog with get_localized_changelog(target_language).

WHAT IT DOES:
- Provides an in-memory container for changelog entries (LocalizedEntry objects) and a default language.
- Allows creation of entries, adding per-language translations by language enum key, and rendering the full changelog in a requested language with graceful fallback to original text.
- Exposes __version__ from the project's lifecycle.version and uses LocalizationLanguage enum keys for translations.

WHAT IT SHOULD DO BETTER:
- Persist entries (file/db) or accept external sources so translations survive process restarts.
- Provide robust locale formatting (dates, lists), pluralization, and markup handling; integrate with gettext or ICU for production-grade i18n.
- Return structured output (e.g., list/dict) alongside plain text rendering and support per-entry metadata (type, scope, severity).
- Validate inputs and languages, surface errors for unknown entries, and document thread-safety / concurrency expectations.
- Add optional async translation hooks, batched translation support via external services, unit tests for edge cases, and better typing (TypedDict/dataclasses) for LocalizedEntry.
"""

from __future__ import annotations

from src.core.base.common.types.localization_language import LocalizationLanguage
from src.core.base.common.types.localized_entry import LocalizedEntry
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ChangelogLocalizer:
    """Handles changelog localization to multiple languages.

    Provides functionality to translate changelog entries to different
    languages for international users.

    Attributes:
        entries: List of localized entries.
        default_language: Default language for entries.

    Example:
        >>> localizer=ChangelogLocalizer()
        >>> entry=localizer.create_entry("Added new feature")
        >>> localizer.add_translation(entry, LocalizationLanguage.SPANISH, "Nueva característica")
    """

    def __init__(self, default_language: LocalizationLanguage = LocalizationLanguage.ENGLISH) -> None:
        """Initialize the changelog localizer.

        Args:
            default_language: Default language for entries.
        """
        self.entries: list[LocalizedEntry] = []
        self.default_language = default_language

    def create_entry(self, text: str) -> LocalizedEntry:
        """Create a new localized entry.

        Args:
            text: Original entry text.

        Returns:
            A new LocalizedEntry instance.
        """
        entry = LocalizedEntry(original_text=text, language=self.default_language)
        self.entries.append(entry)
        return entry

    def add_translation(self, entry: LocalizedEntry, language: LocalizationLanguage, translation: str) -> None:
        """Add a translation to an entry.

        Args:
            entry: The entry to translate.
            language: Target language.
            translation: Translated text.
        """
        entry.translations[language.value] = translation

    def get_localized_changelog(self, language: LocalizationLanguage) -> str:
        """Get the changelog in a specific language.

        Args:
            language: Target language.

        Returns:
            Changelog text in the specified language.
        """
        result: list[str] = []
        for entry in self.entries:
            if language.value in entry.translations:
                result.append(entry.translations[language.value])
            else:
                result.append(entry.original_text)
        return "\n".join(result)
