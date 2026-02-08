# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_gunnerc2.py\core.py\malleable_engine.py\registry_151832f601e9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GunnerC2\core\malleable_engine\registry.py

from __future__ import annotations

from typing import Dict, Type

from .base import ProfileLoader, ProfileParser

PARSERS: Dict[str, Type[ProfileParser]] = {}

LOADERS: Dict[str, Type[ProfileLoader]] = {}


def register_parser(name: str):
    def deco(cls: Type[ProfileParser]):
        PARSERS[name] = cls

        return cls

    return deco


def register_loader(name: str):
    def deco(cls: Type[ProfileLoader]):
        LOADERS[name] = cls

        return cls

    return deco
