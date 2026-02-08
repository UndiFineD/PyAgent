# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tests.py\vocoder_tests.py\test_vocoder_melgan_generator_1e64dd0d7b9f.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\tests\vocoder_tests\test_vocoder_melgan_generator.py

import numpy as np

import torch

from TTS.vocoder.models.melgan_generator import MelganGenerator


def test_melgan_generator():
    model = MelganGenerator()

    print(model)

    dummy_input = torch.rand((4, 80, 64))

    output = model(dummy_input)

    assert np.all(output.shape == (4, 1, 64 * 256))

    output = model.inference(dummy_input)

    assert np.all(output.shape == (4, 1, (64 + 4) * 256))
