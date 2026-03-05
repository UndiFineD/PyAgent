#!/usr/bin/env python3
"""Minimal FlakinessDetector shim."""


class FlakinessDetector:
    def detect(self, results):
        return False


__all__ = ["FlakinessDetector"]
