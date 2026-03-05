#!/usr/bin/env python3
"""Minimal EnvironmentIsolator shim."""


class EnvironmentIsolator:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


__all__ = ["EnvironmentIsolator"]
