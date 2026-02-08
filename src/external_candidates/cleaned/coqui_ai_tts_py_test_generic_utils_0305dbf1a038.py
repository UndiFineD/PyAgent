# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\coqui_ai_tts.py\tests.py\aux_tests.py\test_generic_utils_0305dbf1a038.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\tests\aux_tests\test_generic_utils.py

import pytest

from TTS.utils.generic_utils import slugify


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        # ASCII-safe names
        ("Craig Gutsy", "Craig_Gutsy"),
        ("Dr.Jane", "Dr_Jane"),
        ("Mr-Smith_01", "Mr-Smith_01"),
        # Names with accents and spaces
        ("Zoë", "Zoe"),
        ("Renée O'Connor", "Renee_O_Connor"),
        ("Jürgen Müller", "Jurgen_Muller"),
        # Unsafe punctuation and repeated underscores
        ("Hello!!!", "Hello"),
        ("foo///bar", "foo_bar"),
        (" a  b ", "a_b"),
        # Emojis and symbols
        ("Speaker 🔥 #1", "Speaker_1"),
        # Edge cases
        ("", ""),
    ],
)
def test_slugify(input_text, expected_output):
    assert slugify(input_text) == expected_output
