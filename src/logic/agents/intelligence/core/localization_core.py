from __future__ import annotations
from typing import Any
import re

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class LocalizationCore:
    """
    LocalizationCore handles translation logic (placeholder) and Cultural Guardrails.
    It identifies problematic idioms or metaphors in multi-agent communication.
    """

    def __init__(self) -> None:
        # List of potentially offensive or culturally insensitive metaphors/idioms
        # This is a basic starter list for the guardrail.
        self.cultural_red_flags = [
            r"\bbite the bullet\b",  # Violent metaphor
            r"\bkill two birds\b",  # Violent metaphor
            r"\bdoghouse\b",  # Culturally variable idiom
            r"\bgrandfathered\b",  # Potentially non-inclusive language
            r"\bblackbox\b",  # Potentially non-inclusive language
            r"\bwhitelist\b",  # Potentially non-inclusive language
            r"\bblacklist\b",  # Potentially non-inclusive language
            r"\bsanity check\b",  # Potentially ableist language
        ]

    def detect_cultural_issues(self, text: str) -> list[dict[str, Any]]:
        """
        Detects cultural red flags in agent communication.
        Returns a list of identified issues with suggestions.
        """
        if HAS_RUST:
            try:
                # Rust implementation expects regex patterns
                return rust_core.detect_cultural_issues(text, self.cultural_red_flags)  # type: ignore[attr-defined]
            except Exception:
                pass

        issues = []
        for pattern in self.cultural_red_flags:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                issues.append(
                    {
                        "term": match.group(),
                        "index": match.start(),
                        "severity": "low",
                        "suggestion": "Consider more direct or inclusive technical language.",
                    }
                )
        return issues

    def get_supported_locales(self) -> list[str]:
        """Returns the 12 major languages currently prioritized for translation."""
        return ["en", "zh", "es", "hi", "ar", "bn", "pt", "ru", "ja", "de", "fr", "ko"]

    def format_translation_request(self, text: str, target_lang: str) -> str:
        """Constructs a prompt or request for an external translation service (DeepL/LLM)."""
        return f"Translate the following technical agent comment to {target_lang}:\n\n{text}"
