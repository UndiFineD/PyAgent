# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-OpenWhisper-clone\services\__init__.py
"""
Services package - core business logic and managers.
"""

from services.audio_processor import AudioFilePreview, AudioProcessor, audio_processor
from services.history_manager import (
    HistoryEntry,
    HistoryManager,
    RecordingInfo,
    history_manager,
)
from services.hotkey_manager import HotkeyManager
from services.recorder import AudioRecorder
from services.settings import SettingsManager, settings_manager

__all__ = [
    "AudioRecorder",
    "audio_processor",
    "AudioProcessor",
    "AudioFilePreview",
    "HotkeyManager",
    "history_manager",
    "HistoryManager",
    "HistoryEntry",
    "RecordingInfo",
    "settings_manager",
    "SettingsManager",
]
