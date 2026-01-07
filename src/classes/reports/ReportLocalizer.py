#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .LocaleCode import LocaleCode
from .LocalizedString import LocalizedString

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

class ReportLocalizer:
    """Localizer for report internationalization.
    Handles translation of report strings.
    Attributes:
        strings: Localized strings.
        current_locale: Current locale.
    Example:
        localizer=ReportLocalizer()
        localizer.add_string("error.syntax", {"en-US": "Syntax Error"})
        text=localizer.get("error.syntax")
    """

    def __init__(self, locale: LocaleCode = LocaleCode.EN_US) -> None:
        """Initialize localizer.
        Args:
            locale: Default locale.
        """

        self.strings: Dict[str, LocalizedString] = {}
        self.current_locale = locale
        self._init_defaults()
        logging.debug(f"ReportLocalizer initialized with {locale.value}")

    def _init_defaults(self) -> None:
        """Initialize default strings."""

        defaults = {
            "report.description": {"en-US": "Description", "de-DE": "Beschreibung"},
            "report.errors": {"en-US": "Errors", "de-DE": "Fehler"},
            "report.improvements": {"en-US": "Improvements", "de-DE": "Verbesserungen"},
            "severity.info": {"en-US": "Info", "de-DE": "Info"},
            "severity.warning": {"en-US": "Warning", "de-DE": "Warnung"},
            "severity.error": {"en-US": "Error", "de-DE": "Fehler"},
        }
        for key, translations in defaults.items():
            self.add_string(key, translations)

    def add_string(self, key: str, translations: Dict[str, str]) -> None:
        """Add a localized string.
        Args:
            key: String key.
            translations: Locale to text mapping.
        """

        default = translations.get("en-US", list(translations.values())[0] if translations else "")
        self.strings[key] = LocalizedString(key=key, translations=translations, default=default)

    def get(self, key: str, locale: Optional[LocaleCode] = None) -> str:
        """Get localized string.
        Args:
            key: String key.
            locale: Override locale.
        Returns:
            Localized text.
        """

        loc = locale or self.current_locale
        if key not in self.strings:
            return key
        string = self.strings[key]
        return string.translations.get(loc.value, string.default)

    def set_locale(self, locale: LocaleCode) -> None:
        """Set current locale.
        Args:
            locale: New locale.
        """

        self.current_locale = locale
