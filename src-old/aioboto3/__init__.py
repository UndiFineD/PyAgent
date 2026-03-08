"""Minimal aioboto3 shim providing an async context manager client."""
from __future__ import annotations
import boto3


class _AsyncClientCM:
    def __init__(self, service_name, **kwargs):
        self._service_name = service_name
        self._kwargs = kwargs
        self._client = None

    async def __aenter__(self):
        # create a synchronous dummy client and return it
        self._client = boto3.client(self._service_name, **self._kwargs)
        return self._client

    async def __aexit__(self, exc_type, exc, tb):
        # nothing to close for dummy client
        return False


def client(service_name, **kwargs):
    """Return an async context manager that yields a dummy boto3 client."""
    return _AsyncClientCM(service_name, **kwargs)

__all__ = ["client"]
"""Minimal aioboto3 shim for tests.
Provides an async-capable `client()` factory that returns a dummy client.
"""
__all__ = ["client"]

class _AsyncDummyClient:
    def __init__(self, service_name):
        self._service = service_name

    def __getattr__(self, item):
        async def _missing(*args, **kwargs):
            raise NotImplementedError(f"aioboto3.{self._service}.{item} is not implemented in test shim")
        return _missing

async def client(service_name, *args, **kwargs):
    return _AsyncDummyClient(service_name)
