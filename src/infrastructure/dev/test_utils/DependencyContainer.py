#!/usr/bin/env python3
"""Minimal DependencyContainer shim."""


class DependencyContainer:
    def __init__(self):
        self._deps = {}

    def register(self, name, obj):
        self._deps[name] = obj

    def resolve(self, name, default=None):
        return self._deps.get(name, default)


__all__ = ["DependencyContainer"]
