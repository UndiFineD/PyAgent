
"""
Core logic for Data Privacy (Phase 171).
Handles PII detection and redaction using regex.
"""

import re
from typing import Dict

class PrivacyCore:
    # Patterns for sensitive data
    PATTERNS = {
        "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        "api_key": r'(?:key|token|auth|secret|password)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-\.\~]{16,})["\']?',
        "ipv4": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "credit_card": r'\b(?:\d[ -]*?){13,16}\b'
    }

    @classmethod
    def redact_text(cls, text: str) -> str:
        """
        Scans text for PII and replaces it with [REDACTED].
        """
        redacted = text
        for label, pattern in cls.PATTERNS.items():
            if label == "api_key":
                # For API keys, we want to redact the value part captured in group 1
                matches = re.finditer(pattern, redacted, re.IGNORECASE)
                offset = 0
                for match in matches:
                    val = match.group(1)
                    start = match.start(1) + offset
                    end = match.end(1) + offset
                    redacted = redacted[:start] + "[REDACTED_API_KEY]" + redacted[end:]
                    offset += len("[REDACTED_API_KEY]") - len(val)
            else:
                redacted = re.sub(pattern, f"[REDACTED_{label.upper()}]", redacted)
        return redacted

    @classmethod
    def scan_log_entry(cls, entry: Dict) -> Dict:
        """
        Recursively redacts sensitive info from a log dictionary.
        """
        if isinstance(entry, dict):
            return {k: cls.scan_log_entry(v) for k, v in entry.items()}
        elif isinstance(entry, list):
            return [cls.scan_log_entry(i) for i in entry]
        elif isinstance(entry, str):
            return cls.redact_text(entry)
        return entry