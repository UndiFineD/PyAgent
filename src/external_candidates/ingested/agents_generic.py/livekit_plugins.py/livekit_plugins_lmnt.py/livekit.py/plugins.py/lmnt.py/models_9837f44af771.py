# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-lmnt\livekit\plugins\lmnt\models.py
from typing import Literal

LMNTAudioFormats = Literal["aac", "mp3", "mulaw", "raw", "wav"]
LMNTLanguages = Literal[
    "auto",
    "de",
    "en",
    "es",
    "fr",
    "hi",
    "id",
    "it",
    "ja",
    "ko",
    "nl",
    "pl",
    "pt",
    "ru",
    "sv",
    "th",
    "tr",
    "uk",
    "vi",
    "zh",
]
LMNTModels = Literal["blizzard", "aurora"]
LMNTSampleRate = Literal[8000, 16000, 24000]
