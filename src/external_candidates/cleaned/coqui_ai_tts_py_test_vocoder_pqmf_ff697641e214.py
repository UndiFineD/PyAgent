# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tests.py\vocoder_tests.py\test_vocoder_pqmf_ff697641e214.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\tests\vocoder_tests\test_vocoder_pqmf.py

import os

import soundfile as sf

import torch

from librosa.core import load

from TTS.vocoder.layers.pqmf import PQMF

from tests import get_tests_input_path

WAV_FILE = os.path.join(get_tests_input_path(), "example_1.wav")


def test_pqmf(tmp_path):
    w, sr = load(WAV_FILE)

    layer = PQMF(N=4, taps=62, cutoff=0.15, beta=9.0)

    w, sr = load(WAV_FILE)

    w2 = torch.from_numpy(w[None, None, :])

    b2 = layer.analysis(w2)

    w2_ = layer.synthesis(b2)

    print(w2_.max())

    print(w2_.min())

    print(w2_.mean())

    sf.write(tmp_path / "pqmf_output.wav", w2_.flatten().detach(), sr)
