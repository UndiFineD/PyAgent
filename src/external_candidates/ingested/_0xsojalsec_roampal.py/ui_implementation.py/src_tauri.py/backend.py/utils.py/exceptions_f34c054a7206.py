# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-roampal\ui-implementation\src-tauri\backend\utils\exceptions.py
class OGException(Exception):
    """Base exception for Roampal OG system."""

    pass


class OllamaException(OGException):
    """Exception for Ollama-specific errors."""

    pass
