class ClientError(Exception):
    """Minimal ClientError shim for tests that import botocore.exceptions.ClientError."""
    def __init__(self, error_response=None, operation_name=None):
        self.response = error_response
        self.operation_name = operation_name
        super().__init__(str(error_response) if error_response is not None else operation_name)

__all__ = ["ClientError"]
"""Minimal exceptions submodule for botocore shim."""
class ClientError(Exception):
    def __init__(self, error_response=None, operation_name=None):
        self.response = error_response or {}
        self.operation_name = operation_name
        super().__init__(f"ClientError: {self.response}")

class BotoCoreError(Exception):
    pass

__all__ = ["ClientError", "BotoCoreError"]
