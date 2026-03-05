#!/usr/bin/env python3
"""Minimal DependencyResolver shim."""


class DependencyResolver:
    def __init__(self, container=None):
        self.container = container

    def resolve(self, name):
        if self.container:
            return self.container.resolve(name)
        return None


__all__ = ["DependencyResolver"]
