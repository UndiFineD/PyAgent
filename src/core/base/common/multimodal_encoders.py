#!/usr/bin/env python3
from __future__ import annotations

"""Minimal multimodal encoders shim.

Provides simple encode helpers used by other modules during repairs.
"""
from typing import Any


def encode_to_bytes(obj: Any) -> bytes:
    """Conservative encoder that stringifies objects."""
    if obj is None:
        return b""
    if isinstance(obj, bytes):
        return obj
    return str(obj).encode("utf-8")


class Encoder:
    def encode(self, obj: Any) -> bytes:
        return encode_to_bytes(obj)
