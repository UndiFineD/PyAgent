# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-plugins\livekit-plugins-turn-detector\livekit\plugins\turn_detector\models.py
from typing import Literal

EOUModelType = Literal["en", "multilingual"]
MODEL_REVISIONS: dict[EOUModelType, str] = {
    "en": "v1.2.2-en",
    "multilingual": "v0.3.0-intl",
}
HG_MODEL = "livekit/turn-detector"
ONNX_FILENAME = "model_q8.onnx"
