# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-smallestai\livekit\plugins\smallestai\models.py
from typing import Literal

TTSModels = Literal[
    "lightning",
    "lightning-large",
    "lightning-v2",
]

TTSEncoding = Literal[
    "pcm",
    "mp3",
    "wav",
    "mulaw",
]
