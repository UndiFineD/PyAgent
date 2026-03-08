"""Lightweight boto3 shim used by tests when the real library is not required."""
class _DummyClient:
    def __init__(self, service_name, **kwargs):
        self.service_name = service_name
        self._kwargs = kwargs

    def __repr__(self):
        return f"<DummyBoto3Client service={self.service_name}>"

    # Provide a safe stub for attribute access used by tests
    def __getattr__(self, name):
        def _stub(*args, **kwargs):
            return None
        return _stub


def client(service_name, **kwargs):
    """Return a dummy client object compatible with simple uses in tests."""
    return _DummyClient(service_name, **kwargs)

__all__ = ["client"]
"""Minimal boto3 shim for tests.
Expose a `client()` factory returning a lightweight stub client.
"""
__all__ = ["client"]

class _DummyClient:
    def __init__(self, service_name):
        self._service = service_name

    def __getattr__(self, item):
        def _missing(*args, **kwargs):
            raise NotImplementedError(f"boto3.{self._service}.{item} is not implemented in test shim")
        return _missing

def client(service_name, *args, **kwargs):
    return _DummyClient(service_name)
