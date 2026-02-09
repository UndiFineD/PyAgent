# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Newelle\src\handlers\tts\__init__.py
from .custom_handler import CustomTTSHandler
from .custom_openai_tts import CustomOpenAITTSHandler
from .elevenlabs_handler import ElevenLabs
from .espeak_handler import EspeakHandler
from .groq_tts_handler import GroqTTSHandler
from .gtts_handler import gTTSHandler
from .kokoro_handler import KokoroTTSHandler
from .openai_tts_handler import OpenAITTSHandler
from .tts import TTSHandler

__all__ = [
    "TTSHandler",
    "CustomTTSHandler",
    "EspeakHandler",
    "gTTSHandler",
    "ElevenLabs",
    "KokoroTTSHandler",
    "OpenAITTSHandler",
    "CustomOpenAITTSHandler",
    "GroqTTSHandler",
]
