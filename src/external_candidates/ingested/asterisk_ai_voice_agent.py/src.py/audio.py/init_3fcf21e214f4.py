# Extracted from: C:\DEV\PyAgent\.external\Asterisk-AI-Voice-Agent\src\audio\__init__.py
"""
Audio processing utilities for the Asterisk AI Voice Agent.

This package contains audio processing helpers and utilities.
"""

from .resampler import (
    convert_pcm16le_to_target_format,
    mulaw_to_pcm16le,
    pcm16le_to_mulaw,
    resample_audio,
)

__all__ = [
    "mulaw_to_pcm16le",
    "pcm16le_to_mulaw",
    "resample_audio",
    "convert_pcm16le_to_target_format",
]
