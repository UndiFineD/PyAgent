"""Root shim re-exporting `scripts.boto3` to satisfy imports during tests.
"""
from importlib import import_module

_mod = import_module("scripts.boto3")

client = getattr(_mod, "client")

__all__ = ["client"]
