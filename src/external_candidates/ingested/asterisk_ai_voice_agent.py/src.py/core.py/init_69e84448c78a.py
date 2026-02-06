# Extracted from: C:\DEV\PyAgent\.external\Asterisk-AI-Voice-Agent\src\core\__init__.py
"""
Core modules for the Asterisk AI Voice Agent.

This package contains the centralized state management and playback
management components that replace the dict soup in the original engine.
"""

from .conversation_coordinator import ConversationCoordinator
from .models import CallSession, PlaybackRef, ProviderSession, TransportConfig
from .playback_manager import PlaybackManager
from .session_store import SessionStore

__all__ = [
    "CallSession",
    "PlaybackRef",
    "ProviderSession",
    "TransportConfig",
    "SessionStore",
    "PlaybackManager",
    "ConversationCoordinator",
]
