#!/usr/bin/env python3
"""Minimal FlakinessReport shim."""


class FlakinessReport:
    def __init__(self, *_, **__):
        self.issues = []

    def add(self, item):
        self.issues.append(item)


__all__ = ["FlakinessReport"]
