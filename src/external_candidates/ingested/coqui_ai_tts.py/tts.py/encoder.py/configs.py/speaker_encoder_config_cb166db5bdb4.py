# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\TTS\encoder\configs\speaker_encoder_config.py
from dataclasses import dataclass

from TTS.encoder.configs.base_encoder_config import BaseEncoderConfig


@dataclass
class SpeakerEncoderConfig(BaseEncoderConfig):
    """Defines parameters for Speaker Encoder model."""

    model: str = "speaker_encoder"
    class_name_key: str = "speaker_name"
