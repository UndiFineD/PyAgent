# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-google\livekit\plugins\google\beta\__init__.py
from . import realtime
from .gemini_tts import TTS as GeminiTTS

__all__ = ["realtime", "GeminiTTS"]

# Cleanup docs of unexported modules
_module = dir()
NOT_IN_ALL = [m for m in _module if m not in __all__]

__pdoc__ = {}

for n in NOT_IN_ALL:
    __pdoc__[n] = False
