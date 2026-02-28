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
