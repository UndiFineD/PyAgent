#!/usr/bin/env python3
"""SnapshotComparisonResult shim for pytest collection."""


class SnapshotComparisonResult:
    def __init__(self, baseline=None, current=None, diffs=None):
        self.baseline = baseline
        self.current = current
        self.diffs = diffs or []

    def is_equal(self):
        return not bool(self.diffs)


__all__ = ["SnapshotComparisonResult"]
