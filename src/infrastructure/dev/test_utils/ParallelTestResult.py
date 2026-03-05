#!/usr/bin/env python3
"""Minimal ParallelTestResult shim."""


class ParallelTestResult:
    def __init__(self):
        self.results = []

    def add(self, res):
        self.results.append(res)


__all__ = ["ParallelTestResult"]
