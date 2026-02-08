# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\pypirc_0bbed58bb227.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\pypirc.py

from pathlib import Path


class Pypirc:
    def pairs(self, filepath: Path):
        for line in filepath.open("r").readlines():
            if "password:" not in line:
                continue

            value = line.split("password:")[-1].strip()

            if value:
                yield "PyPI_Password", value
