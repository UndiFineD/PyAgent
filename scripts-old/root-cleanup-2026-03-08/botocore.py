"""Root shim re-exporting `scripts.botocore` to satisfy imports during tests.
The real minimal implementation lives in `scripts/botocore.py`.
"""
from importlib import import_module

_mod = import_module("scripts.botocore")

ClientError = _mod.ClientError

__all__ = ["ClientError"]
