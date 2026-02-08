# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\jproperties_75e8a9da5333.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\jproperties.py

from pathlib import Path

from jproperties import Properties


class Jproperties:
    def pairs(self, filepath: Path):

        props = Properties()

        props.load(filepath.read_text(), "utf-8")

        for key, value in props.properties.items():
            key = key.replace(".", "_")

            yield key, value
