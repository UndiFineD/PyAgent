"""Lightweight botocore shim for tests when AWS SDK is not installed.
This provides minimal classes/exceptions used by the codebase to avoid
import-time failures. If used at runtime these stubs raise clear errors.
"""
class ClientError(Exception):
    pass

__all__ = ["ClientError"]
