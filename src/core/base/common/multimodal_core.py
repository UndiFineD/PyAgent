#!/usr/bin/env python3
from __future__ import annotations

"""Lightweight multimodal core shim.

Minimal, importable helpers for multimodal processing used during repair.
"""
from typing import Any, Dict


class MultimodalCore:
    def __init__(self) -> None:
        pass

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return payload unmodified as a safe default."""
        return payload

    def encode(self, data: Any) -> bytes:
        return str(data).encode() if data is not None else b""
