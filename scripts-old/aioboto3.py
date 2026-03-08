"""Lightweight aioboto3 shim placed in `scripts/` per repository conventions.
Provides a minimal async `client` context manager that raises if used.
"""
from contextlib import asynccontextmanager

__all__ = ["client"]

@asynccontextmanager
async def client(*args, **kwargs):
    class _Dummy:
        async def __aenter__(self_inner):
            raise RuntimeError("aioboto3 is not installed in this environment")

        async def __aexit__(self_inner, exc_type, exc, tb):
            return False

    yield _Dummy()
