# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-anam\livekit\plugins\anam\types.py
from dataclasses import dataclass


@dataclass
class PersonaConfig:
    """Configuration for Anam avatar persona"""

    name: str
    avatarId: str
