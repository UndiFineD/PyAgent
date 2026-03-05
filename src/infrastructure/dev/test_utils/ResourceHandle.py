#!/usr/bin/env python3
"""ResourceHandle shim for pytest collection."""


class ResourceHandle:
    def __init__(self, identifier: str, resource=None):
        self.id = identifier
        self.resource = resource

    def release(self):
        self.resource = None


__all__ = ["ResourceHandle"]
