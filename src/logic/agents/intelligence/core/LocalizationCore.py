from __future__ import annotations
from typing import Dict, List, Any, Optional
import re

class LocalizationCore:
    """
    LocalizationCore handles translation logic (placeholder) and Cultural Guardrails.
    It identifies problematic idioms or metaphors in multi-agent communication.
    """

    def __init__(self) -> None:
        # List of potentially offensive or culturally insensitive metaphors/idioms
        # This is a basic starter list for the guardrail.
        self.cultural_red_flags = [
            r"\bbite the bullet\b",      # Violent metaphor
            r"\bkill two birds\b",       # Violent metaphor
            r"\bdoghouse\b",             # Culturally variable idiom
            r"\bgrandfathered\b",        # Potentially non-inclusive language
            r"\bblackbox\b",             # Potentially non-inclusive language
            r"\bwhitelist\b",            # Potentially non-inclusive language
            r"\bblacklist\b",            # Potentially non-inclusive language
            r"\bsanity check\b"          # Potentially ableist language
        ]

    def detect_cultural_issues(self, text: str) -> List[Dict[str, Any]]:
        """
        Detects cultural red flags in agent communication.
        Returns a list of identified issues with suggestions.
        """
        issues = []
        for pattern in self.cultural_red_flags:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                issues.append({
                    "term": match.group(),
                    "index": match.start(),
                    "severity": "low",
                    "suggestion": "Consider more direct or inclusive technical language."
                })
        return issues

    def get_supported_locales(self) -> List[str]:
        """Returns the 12 major languages currently prioritized for translation."""
        return [
            "en", "zh", "es", "hi", "ar", 
            "bn", "pt", "ru", "ja", "de", 
            "fr", "ko"
        ]

    def format_translation_request(self, text: str, target_lang: str) -> str:
        """Constructs a prompt or request for an external translation service (DeepL/LLM)."""
        return f"Translate the following technical agent comment to {target_lang}:\n\n{text}"
