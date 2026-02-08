# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tts.py\tts.py\configs.py\tacotron2_config_0ba1170dc757.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\TTS\tts\configs\tacotron2_config.py

from dataclasses import dataclass

from TTS.tts.configs.tacotron_config import TacotronConfig


@dataclass
class Tacotron2Config(TacotronConfig):
    """Defines parameters for Tacotron2 based models.

    Example:

        >>> from TTS.tts.configs.tacotron2_config import Tacotron2Config

        >>> config = Tacotron2Config()

    Check `TacotronConfig` for argument descriptions.

    """

    model: str = "tacotron2"

    out_channels: int = 80

    encoder_in_features: int = 512

    decoder_in_features: int = 512
