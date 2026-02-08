# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tts.py\vc.py\layers.py\freevc.py\wavlm.py\init_ce44ea632925.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\TTS\vc\layers\freevc\wavlm\__init__.py

import logging

import os

import urllib.request

import torch

from trainer.io import get_user_data_dir

from TTS.utils.generic_utils import is_pytorch_at_least_2_4

from TTS.vc.layers.freevc.wavlm.wavlm import WavLM, WavLMConfig

logger = logging.getLogger(__name__)

model_uri = "https://github.com/coqui-ai/TTS/releases/download/v0.13.0_models/WavLM-Large.pt"


def get_wavlm(device="cpu") -> WavLM:
    """Download the model and return the model object."""

    output_path = get_user_data_dir("tts")

    output_path = os.path.join(output_path, "wavlm")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_path = os.path.join(output_path, "WavLM-Large.pt")

    if not os.path.exists(output_path):
        logger.info("Downloading WavLM model to %s ...", output_path)

        urllib.request.urlretrieve(model_uri, output_path)

    checkpoint = torch.load(
        output_path,
        map_location=torch.device(device),
        weights_only=is_pytorch_at_least_2_4(),
    )

    cfg = WavLMConfig(checkpoint["cfg"])

    wavlm = WavLM(cfg).to(device)

    wavlm.load_state_dict(checkpoint["model"])

    wavlm.eval()

    return wavlm


if __name__ == "__main__":
    wavlm = get_wavlm()
