#!/usr/bin/env python3
"""Minimal CoverageTracker shim."""


class CoverageTracker:
    def __init__(self, *_, **__):
        self.records = []

    def track(self, name):
        self.records.append(name)


__all__ = ["CoverageTracker"]
