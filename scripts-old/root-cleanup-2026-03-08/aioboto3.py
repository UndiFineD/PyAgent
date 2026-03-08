"""Compatibility shim: re-export `client` from `scripts.aioboto3`.

The real implementation lives in `scripts/aioboto3.py` per project policy.
"""
from importlib import import_module

_mod = import_module("scripts.aioboto3")

client = getattr(_mod, "client")

__all__ = ["client"]
