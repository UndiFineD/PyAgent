# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\whispers.py\plugins.py\dockercfg_6b82c3c8e20b.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\dockercfg.py

import json

from pathlib import Path


class Dockercfg:
    def pairs(self, filepath: Path):

        config = json.loads(filepath.read_text())

        if "auths" not in config:
            return

        for auth in config["auths"].values():
            if "auth" not in auth:
                continue

            token = auth["auth"]

            yield "Dockercfg", token
