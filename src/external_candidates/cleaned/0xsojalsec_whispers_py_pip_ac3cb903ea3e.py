# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\pip_ac3cb903ea3e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\pip.py

from pathlib import Path

from urllib.parse import urlparse


class Pip:
    def pairs(self, filepath: Path):
        for line in filepath.open("r").readlines():
            if "http" not in line:
                continue

            value = urlparse(line.split("=")[-1].strip()).password

            if value:
                yield "pip_Password", value
