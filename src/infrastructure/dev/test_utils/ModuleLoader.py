#!/usr/bin/env python3
"""Minimal ModuleLoader shim."""


class ModuleLoader:
    def load(self, name):
        try:
            __import__(name)
            return True
        except Exception:
            return False


__all__ = ["ModuleLoader"]
