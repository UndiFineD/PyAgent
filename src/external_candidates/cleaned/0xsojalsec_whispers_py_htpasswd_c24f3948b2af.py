# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\htpasswd_c24f3948b2af.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\htpasswd.py

from pathlib import Path

from whispers.utils import strip_string


class Htpasswd:
    def pairs(self, filepath: Path):

        for line in filepath.open("r").readlines():
            if ":" not in line:
                continue

            creds = line.split(":")

            value = strip_string(creds[1])

            if value:
                yield "htpasswd_Hash", value
