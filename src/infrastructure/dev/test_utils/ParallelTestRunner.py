#!/usr/bin/env python3
"""Minimal ParallelTestRunner shim."""


class ParallelTestRunner:
    def __init__(self, *_, **__):
        pass

    def run(self, tests):
        for t in tests:
            t()


__all__ = ["ParallelTestRunner"]
