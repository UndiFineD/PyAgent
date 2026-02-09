# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\tests\aux_tests\test_compute_statistics.py
from pathlib import Path

from TTS.bin.compute_statistics import main

from tests import get_tests_input_path, run_main


def test_compute_statistics(tmp_path):
    config_path = Path(get_tests_input_path()) / "test_glow_tts_config.json"
    output_path = tmp_path / "scale_stats.npy"
    run_main(main, ["--config_path", str(config_path), "--out_path", str(output_path)])
