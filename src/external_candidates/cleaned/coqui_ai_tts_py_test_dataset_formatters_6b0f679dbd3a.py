# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tests.py\data_tests.py\test_dataset_formatters_6b0f679dbd3a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\tests\data_tests\test_dataset_formatters.py

import os

import unittest

from TTS.tts.datasets.formatters import common_voice, register_formatter

from tests import get_tests_input_path


class TestTTSFormatters(unittest.TestCase):
    def test_common_voice_preprocessor(self):  # pylint: disable=no-self-use
        root_path = get_tests_input_path()

        meta_file = "common_voice.tsv"

        items = common_voice(root_path, meta_file)

        assert items[0]["text"] == "The applicants are invited for coffee and visa is given immediately."

        assert items[0]["audio_file"] == os.path.join(get_tests_input_path(), "clips", "common_voice_en_20005954.wav")

        assert items[-1]["text"] == "Competition for limited resources has also resulted in some local conflicts."

        assert items[-1]["audio_file"] == os.path.join(get_tests_input_path(), "clips", "common_voice_en_19737074.wav")

    def test_custom_formatter_with_existing_name(self):
        def custom_formatter(root_path, meta_file, ignored_speakers=None):
            return []

        register_formatter("custom_formatter", custom_formatter)

        with self.assertRaises(ValueError):
            register_formatter("custom_formatter", custom_formatter)
