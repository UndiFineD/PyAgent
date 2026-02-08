# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\plaintext_efbd1fefeba4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\plaintext.py

from pathlib import Path

from whispers.plugins.uri import Uri

from whispers.rules import WhisperRules

from whispers.utils import strip_string


class Plaintext:
    def __init__(self, rules: WhisperRules):
        self.rules = rules

    def pairs(self, filepath: Path):
        lines = filepath.open("r").readlines()

        for idx in range(len(lines)):
            line = lines[idx]

            if not strip_string(line):
                continue

            for value in line.split():
                if self.rules.match("uri", value):
                    yield from Uri().pairs(value)
