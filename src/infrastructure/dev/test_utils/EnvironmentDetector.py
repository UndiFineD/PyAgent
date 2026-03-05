#!/usr/bin/env python3
"""Minimal EnvironmentDetector shim."""


class EnvironmentDetector:
    def is_ci(self):
        return False


__all__ = ["EnvironmentDetector"]
