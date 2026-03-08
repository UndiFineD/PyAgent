"""Minimal boto3 shim that exposes a `client` factory raising on use.
Placed in `scripts/` per repo convention.
"""
def client(*args, **kwargs):
    raise RuntimeError("boto3 is not installed in this environment")

__all__ = ["client"]
