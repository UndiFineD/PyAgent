# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-rime\livekit\plugins\rime\models.py
from typing import Literal

TTSModels = Literal["mistv2", "arcana"]

# https://docs.rime.ai/api-reference/voices
ArcanaVoices = Literal[
    "luna", "celeste", "orion", "ursa", "astra", "esther", "estelle", "andromeda"
]

DefaultMistv2Voice = "cove"
