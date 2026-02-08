# Extracted from: C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_roampal_exceptions.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-roampal\ui-implementation\src-tauri\backend\utils\exceptions.py
# NOTE: extracted with static-only rules; review before use
class OGException(Exception):
    """Base exception for Roampal OG system."""

    pass


class OllamaException(OGException):
    """Exception for Ollama-specific errors."""

    pass
