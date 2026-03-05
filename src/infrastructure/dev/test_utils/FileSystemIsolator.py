#!/usr/bin/env python3
"""Minimal FileSystemIsolator shim."""


class FileSystemIsolator:
    def __init__(self, *_, **__):
        pass

    def setup(self):
        return None

    def teardown(self):
        return None


__all__ = ["FileSystemIsolator"]
