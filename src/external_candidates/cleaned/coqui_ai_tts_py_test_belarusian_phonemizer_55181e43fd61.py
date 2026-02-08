# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tests.py\text_tests.py\test_belarusian_phonemizer_55181e43fd61.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\tests\text_tests\test_belarusian_phonemizer.py

import os

import unittest

import warnings

from TTS.tts.utils.text.belarusian.phonemizer import belarusian_text_to_phonemes

_TEST_CASES = """

Фанетычны канвертар/fanʲɛˈtɨt͡ʂnɨ kanˈvʲɛrtar

Гэтак мы працавалі/ˈɣɛtak ˈmɨ prat͡saˈvalʲi

"""


class TestText(unittest.TestCase):
    def test_belarusian_text_to_phonemes(self):
        try:
            os.environ["BEL_FANETYKA_JAR"]

        except KeyError:
            warnings.warn(
                "You need to define 'BEL_FANETYKA_JAR' environment variable as path to the fanetyka.jar file to test Belarusian phonemizer",
                Warning,
            )

            return

        for line in _TEST_CASES.strip().split("\n"):
            text, phonemes = line.split("/")

            self.assertEqual(belarusian_text_to_phonemes(text), phonemes)


if __name__ == "__main__":
    unittest.main()
