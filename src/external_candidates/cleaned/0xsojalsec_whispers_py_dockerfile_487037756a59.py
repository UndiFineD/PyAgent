# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\dockerfile_487037756a59.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\dockerfile.py

from pathlib import Path


class Dockerfile:
    def pairs(self, filepath: Path):
        for line in filepath.open("r").readlines():
            # ENV key=value

            if line.startswith("ENV "):
                item = line.replace("ENV ", "", 1)

                for op in ["=", " "]:
                    if op in item and len(item.split(op)) == 2:
                        key, value = item.split(op)

                        yield key, value
