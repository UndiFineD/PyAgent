# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_plugins.py\livekit_plugins_anam.py\livekit.py\plugins.py\anam.py\types_f8a10c068337.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-anam\livekit\plugins\anam\types.py

from dataclasses import dataclass


@dataclass
class PersonaConfig:
    """Configuration for Anam avatar persona"""

    name: str

    avatarId: str
