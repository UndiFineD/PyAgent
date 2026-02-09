# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OpenWhisper-clone\transcriber\__init__.py
"""
Transcription backends for the OpenWhisper application.
"""

from .base import TranscriptionBackend
from .local_backend import LocalWhisperBackend
from .openai_backend import OpenAIBackend

__all__ = ["TranscriptionBackend", "LocalWhisperBackend", "OpenAIBackend"]
