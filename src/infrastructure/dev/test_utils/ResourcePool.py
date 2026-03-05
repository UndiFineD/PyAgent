#!/usr/bin/env python3
"""ResourcePool shim for pytest collection."""


class ResourcePool:
    def __init__(self):
        self._resources = []

    def acquire(self):
        return self._resources.pop() if self._resources else None

    def release(self, r):
        self._resources.append(r)


__all__ = ["ResourcePool"]
