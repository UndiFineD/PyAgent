# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\npmrc_ff93cd09bba6.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\npmrc.py

from pathlib import Path


class Npmrc:
    def pairs(self, filepath: Path):
        for line in filepath.open("r").readlines():
            if ":_authToken=" not in line:
                continue

            value = line.split(":_authToken=")[-1].strip()

            if value:
                yield "npm_authToken", value
