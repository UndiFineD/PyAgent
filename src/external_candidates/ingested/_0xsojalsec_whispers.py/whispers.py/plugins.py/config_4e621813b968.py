# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\whispers\plugins\config.py
from pathlib import Path

from whispers.utils import strip_string


class Config:
    def pairs(self, filepath: Path):
        for line in filepath.open("r").readlines():
            line = line.strip()
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = strip_string(key)
            value = strip_string(value)

            if value:
                yield key, value
