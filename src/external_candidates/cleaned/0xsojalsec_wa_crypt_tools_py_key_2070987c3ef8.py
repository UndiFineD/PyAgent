# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_wa_crypt_tools.py\src.py\wa_crypt_tools.py\lib.py\key.py\key_2070987c3ef8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-wa-crypt-tools\src\wa_crypt_tools\lib\key\key.py

from __future__ import annotations

import abc


class Key(abc.ABC):
    @abc.abstractmethod
    def __init__(self, keyarray: bytes = None):
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def get(self) -> bytes:
        pass

    @abc.abstractmethod
    def dump(self) -> bytes:
        pass
