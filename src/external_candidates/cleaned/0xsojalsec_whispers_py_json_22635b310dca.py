# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\json_22635b310dca.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\json.py

import json

import re

from pathlib import Path

from whispers.log import debug

from whispers.plugins.traverse import StructuredDocument


class Json(StructuredDocument):
    def pairs(self, filepath: Path):
        """

        Convert custom JSON to parsable JSON

        - Remove lines that start with // comments

        - Strip // comments from the end the line

        """

        document = ""

        for line in filepath.open("r").readlines():
            if line.startswith("//"):
                continue

            line = re.sub(r" // ?.*$", "", line)

            document += line

        # Load converted JSON

        try:
            document = json.loads(document)

            yield from self.traverse(document)

        except Exception as e:
            debug(f"{type(e)} in {filepath}")
